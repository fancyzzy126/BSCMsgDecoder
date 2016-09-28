// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

if (typeof Node == "undefined") {
	window.Node = {
		ELEMENT_NODE:1,
		ATTRIBUTE_NODE:2,
		TEXT_NODE:3,
		CDATA_SECTION_NODE:4,
		ENTITY_REFERENCE_NODE:5,
		ENTITY_NODE:6,
		PROCESSING_INSTRUCTION_NODE:7,
		COMMENT_NODE:8,
		DOCUMENT_NODE:9,
		DOCUMENT_TYPE_NODE:10,
		DOCUMENT_FRAGMENT_NODE:11,
		NOTATION_NODE:12
	}
 } 

 if (!document.querySelectorAll) {
    document.querySelectorAll = function (selector) {
        var doc = document,
            head = doc.documentElement.firstChild,
            styleTag = doc.createElement('STYLE');
        head.appendChild(styleTag);
        doc.__qsaels = [];

        if (styleTag.styleSheet) { // for IE
            styleTag.styleSheet.cssText = selector + "{x:expression(document.__qsaels.push(this))}";
        } else { // others
            var textnode = document.createTextNode(selector + "{x:expression(document.__qsaels.push(this))}");
            styleTag.appendChild(textnode);
        }
        window.scrollBy(0, 0);

        return doc.__qsaels;
    }
}

if (!document.querySelector) {
    document.querySelector = function (selectors) {
        var elements = document.querySelectorAll(selectors);
        return (elements.length) ? elements[0] : null;
    };
}

var qsaWorker = (function() {
    var idAllocator = 10000;

    function qsaWorkerShim(element, selector) {
        var needsID = element.id === "";
        if (needsID) {
            ++idAllocator;
            element.id = "__qsa" + idAllocator;
        }
        try {
            return document.querySelectorAll("#" + element.id + " " + selector);
        }
        finally {
            if (needsID) {
                element.id = "";
            }
        }
    }

    function qsaWorkerWrap(element, selector) {
        return element.querySelectorAll(selector);
    }

    // Return the one this browser wants to use
    return document.createElement('div').querySelectorAll ? qsaWorkerWrap : qsaWorkerShim;
})();

function qsWorker(element, selector)
{
	var elements = qsaWorker(element, selector);
	return (elements.length) ? elements[0] : null;
}

function isIE()  
{  
   var i=navigator.userAgent.toLowerCase().indexOf("msie");
   return i>0;
}

function loadXML(str)
{
	var xmldoc;
	if (window.ActiveXObject) {
		//IE
		xmldoc = new ActiveXObject ("Microsoft.XMLDOM");
		xmldoc.async = false;
		xmldoc.loadXML(str);
	} else {
		//Firefox, Mozilla, Opera, Chrome, etc.
		xmldoc = (new DOMParser()).parseFromString(str, "text/xml")
	}
	return xmldoc;
}

///////////////////////////////////////////////////////////////////////

var nodeParentPairs = [];
var tree;

function showXmlGdb(strXmlGdb, id)
{
	tree = createHTMLElement('div');
	//document.body.appendChild(tree);
	tree.className = 'pretty-print';
	tree.id = 'pretty-print' + id;

	var strGDB = strXmlGdb;
	strGDB = strGDB.replace(/<br\/?>/gi, "\n");
	strGDB = strGDB.replace(/&nbsp;/gi, " ");
	//"<repeats 11 times>" is a invalid xml
	strGDB = strGDB.replace(/</g, "(");
	strGDB = strGDB.replace(/>/g, ")");
	//between "{}\n" and "{" is the start line with collapse-button
	//start line does not include the symbol ','	
	strGDB = strGDB.replace(/([^{}\n,]*)({)/g, "<node><start>$1$2</start><div>");
	//between "{" and "{}<>\n" is the end line with expand-button
	//2016-05-12, end line does not include the next field like follows, 
	//as field start with 'a-zA-Z'
	//        }, B_PID_PID = 29
	//2016-05-18, defense the condition as follows:
	//        {
	//          B_TESTERRINFO = 0
	//        } (
	//        repeats 16 times)
	//strGDB = strGDB.replace(/(})([^{}<>\na-zA-Z]*)/g, "</div><end>$1$2</end></node>");
	strGDB = strGDB.replace(/(})([\s]*\([^\)]*\))*([^{}<>\na-zA-Z]*)/g, "</div><end>$1$2$3</end></node>");
	//* = *, after this format, add \n, and output like as follows:
	//B_QUAL_PTR = 0x76 (MP_MSG_WAIT+34),
	//B_MOD_PTR = 0x94 (G_A_Y1EBXV_REMOTE_REQUEST_HDLR+24),
	//B_VALUE = -1,
	//B_MODE = E_OK,
	//{1, 2, 3, 5} this format string still shows in a line
	//strGDB = strGDB.replace(/([0-9a-zA-Z_ -]+)=([0-9a-zA-Z_ -]+)(,)/g, "$1=$2,<br/>");
	strGDB = strGDB.replace(/([^,{}]+)=([^,{}]+)(,)/g, "$1=$2,<br/>");

	strGDB = "<div>" + strGDB + "</div>"; 
	var domGDB = loadXML(strGDB);
	if (domGDB.childNodes.length > 0) {
		nodeParentPairs.push({parentElement: tree, node: domGDB.childNodes[0]});
	}

	for (var i = 0; i < nodeParentPairs.length; i++)
		processElement(nodeParentPairs[i].parentElement, nodeParentPairs[i].node);

	drawArrows();
	initButtons();

	return tree;
}

// Tree processing.

function processElement(parentElement, node)
{
	for (var i = 0; i < node.childNodes.length; i++) {
		var child = node.childNodes[i];
		if ("node" == child.nodeName) {
			var start = child.childNodes[0];
			var content = child.childNodes[1];
			var end = child.childNodes[2];

			var collapsible = createCollapsible();

			collapsible.expanded.start.appendChild(createSpanTag(getTextContent(start)));
			nodeParentPairs.push({parentElement: collapsible.expanded.content, node: content});
			collapsible.expanded.end.appendChild(createSpanTag(getTextContent(end)));

			collapsible.collapsed.content.appendChild(createSpanTag(getTextContent(start)));
			collapsible.collapsed.content.appendChild(document.createTextNode("..."));
			collapsible.collapsed.content.appendChild(createSpanTag(getTextContent(end)));
			parentElement.appendChild(collapsible);

		} else if (Node.TEXT_NODE == child.nodeType && trim(child.nodeValue).length > 0) {
			parentElement.appendChild(createTextTag(child.nodeValue));

		}
	}
}

function createSpanTag(str)
{
	var tag = createHTMLElement('span');
	//tag.classList.add('html-tag');
	tag.className = 'html-tag';

	var text = document.createTextNode(trim(str));
	tag.appendChild(text);

	return tag;
}

function createTextTag(str)
{
	var div = createHTMLElement('div');
	var tag = createHTMLElement('span');
	tag.className = 'html-tag';

	var text = document.createTextNode(trim(str));
	tag.appendChild(text);
	div.appendChild(tag);
	return div
}

function getTextContent(node)
{
	return node.textContent || node.innerText || node.text;
}

// Processing utils.

function trim(value)
{
	return value.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
}

function isShort(value)
{
	return trim(value).length <= 50;
}

// Tree rendering.

function createHTMLElement(elementName)
{
	//return document.createElementNS('http://www.w3.org/1999/xhtml', elementName)
	return document.createElement(elementName)
}

function createCollapsible()
{
	var collapsible = createHTMLElement('div');
	//collapsible.classList.add('collapsible');
	collapsible.className = 'collapsible';
	collapsible.expanded = createHTMLElement('div');
	//collapsible.expanded.classList.add('expanded');
	collapsible.expanded.className = 'expanded';
	collapsible.appendChild(collapsible.expanded);

	collapsible.expanded.start = createLine();
	collapsible.expanded.start.appendChild(createCollapseButton());
	collapsible.expanded.appendChild(collapsible.expanded.start);

	collapsible.expanded.content = createHTMLElement('div');
	//collapsible.expanded.content.classList.add('collapsible-content');
	collapsible.expanded.content.className = 'collapsible-content';
	collapsible.expanded.appendChild(collapsible.expanded.content);

	collapsible.expanded.end = createLine();
	collapsible.expanded.appendChild(collapsible.expanded.end);

	collapsible.collapsed = createHTMLElement('div');
	//collapsible.collapsed.classList.add('collapsed');
	//collapsible.collapsed.classList.add('hidden');
	collapsible.collapsed.className = 'collapsed hidden';
	collapsible.appendChild(collapsible.collapsed);
	collapsible.collapsed.content = createLine();
	collapsible.collapsed.content.appendChild(createExpandButton());
	collapsible.collapsed.appendChild(collapsible.collapsed.content);

	return collapsible;
}

function createButton()
{
	var button;
	if (isIE()) {
		var temp = createHTMLElement('canvas');
		temp.width = 10;
		temp.height = 10;
		document.body.appendChild(temp);
		button = window.G_vmlCanvasManager.initElement(temp);
	} else {
		button = createHTMLElement('span');
	}
	//button.classList.add('button');
	button.className = 'button';
	return button;
}

function createCollapseButton(str)
{
	var button = createButton();
	//button.classList.add('collapse-button');
	button.className += ' collapse-button';
	if (isIE()) {
		var ctx = button.getContext("2d");
		ctx.width = 10;
		ctx.height = 10;
		ctx.fillStyle = "#aa0000";
		ctx.beginPath();
		ctx.moveTo(0, 0);
		ctx.lineTo(8, 0);
		ctx.lineTo(4, 7);
		ctx.lineTo(0, 0);
		ctx.fill();
		ctx.closePath();
	}
	return button;
}

function createExpandButton(str)
{
	var button = createButton();
	//button.classList.add('expand-button');
	button.className += ' expand-button';
	if (isIE()) {
		var ctx = button.getContext("2d");
		ctx.width = 10;
		ctx.height = 10;
		ctx.fillStyle = "#aa0000";
		ctx.beginPath();
		ctx.moveTo(0, 0);
		ctx.lineTo(0, 8);
		ctx.lineTo(7, 4);
		ctx.lineTo(0, 0);
		ctx.fill();
		ctx.closePath();
	}
	return button;
}

function createText(value)
{
	var text = createHTMLElement('span');
	if (isIE) {
		text.innerText = trim(value);
	} else {
		text.textContent = trim(value);
	}
	//text.classList.add('text');
	text.className = 'text';
	return text;
}

function createLine()
{
	var line = createHTMLElement('div');
	//line.classList.add('line');
	line.className = 'line';
	return line;
}

// Tree behaviour.

function drawArrows()
{
	if (!document.getCSSCanvasContext) {
		return
	}

	var ctx = document.getCSSCanvasContext("2d", "arrowRight", 10, 11);

	ctx.fillStyle = "rgb(90,90,90)";
	ctx.beginPath();
	ctx.moveTo(0, 0);
	ctx.lineTo(0, 8);
	ctx.lineTo(7, 4);
	ctx.lineTo(0, 0);
	ctx.fill();
	ctx.closePath();

	var ctx = document.getCSSCanvasContext("2d", "arrowDown", 10, 10);

	ctx.fillStyle = "rgb(90,90,90)";
	ctx.beginPath();
	ctx.moveTo(0, 0);
	ctx.lineTo(8, 0);
	ctx.lineTo(4, 7);
	ctx.lineTo(0, 0);
	ctx.fill();
	ctx.closePath();
}

function expandFunction(domainId, sectionId)
{
	//return function()
	//{
		var domain = document.getElementById(domainId);
		//document.querySelector('#' + sectionId + ' > .expanded').className = 'expanded';
		qsWorker(domain, '#' + sectionId + ' > .expanded').className = 'expanded';
		//document.querySelector('#' + sectionId + ' > .collapsed').className = 'collapsed hidden';
		qsWorker(domain, '#' + sectionId + ' > .collapsed').className = 'collapsed hidden';
	//};
}

function collapseFunction(domainId, sectionId)
{
	//return function()
	//{
		var domain = document.getElementById(domainId);
		//document.querySelector('#' + sectionId + ' > .expanded').className = 'expanded hidden';
		qsWorker(domain, '#' + sectionId + ' > .expanded').className = 'expanded hidden';
		//document.querySelector('#' + sectionId + ' > .collapsed').className = 'collapsed';
		qsWorker(domain, '#' + sectionId + ' > .collapsed').className = 'collapsed';
	//};
}

function initButtons()
{
	//var sections = document.querySelectorAll('.collapsible');
	var sections = qsaWorker(tree, '.collapsible');
	for (var i = 0; i < sections.length; i++) {
		var sectionId = 'collapsible' + i;
		sections[i].id = sectionId;

		var expandedPart = qsWorker(sections[i], '#' + sectionId + ' > .expanded');
		//var expandedPart = sections[i].querySelector('#' + sectionId + ' > .expanded');
		var collapseButton = qsWorker(expandedPart, '.collapse-button');
		//var collapseButton = expandedPart.querySelector('.collapse-button');
		//collapseButton.onclick = collapseFunction(sectionId);
		//collapseButton.onmousedown = handleButtonMouseDown;
		collapseButton.setAttribute('onclick', 'collapseFunction("' + tree.id + '", "' + sectionId + '")');

		var collapsedPart = qsWorker(sections[i], '#' + sectionId + ' > .collapsed');
		//var collapsedPart = sections[i].querySelector('#' + sectionId + ' > .collapsed');
		var expandButton = qsWorker(collapsedPart, '.expand-button');
		//var expandButton = collapsedPart.querySelector('.expand-button');
		//expandButton.onclick = expandFunction(sectionId);
		//expandButton.onmousedown = handleButtonMouseDown;
		expandButton.setAttribute('onclick', 'expandFunction("' + tree.id + '", "' + sectionId + '")');
	}
}

function handleButtonMouseDown(e)
{
   // To prevent selection on double click
   //e.preventDefault();
}

