//global var
__debug_ajax =false ;

function setCookie(name, value, expires, path, domain, secure) {
	var curCookie=name+"="+escape(value)+
		((expires)?"; expires="+expires.toGMTString():"")+
		((path)?"; path="+path:"")+
		((domain)?"; domain="+domain:"")+
		((secure)?"; secure":"");
	//alert("set cookie: " + curCookie);
	document.cookie=curCookie;
}

// returns null if cookie not found
function getCookie(name) {
	var dc=document.cookie;
	//alert("get cookie: " + name + "\ncurrent cookie: " + dc);
	var prefix=name+"=";
	var begin=dc.indexOf("; "+prefix);
	if(begin==-1) {
		begin=dc.indexOf(prefix);
		if(begin!=0)
			return null;
	}
	else
		begin+=2;
	var end=document.cookie.indexOf(";",begin);
	if(end==-1)
		end=dc.length;
	return unescape(dc.substring(begin+prefix.length,end));
}

function deleteCookie(name, path, domain) {
if(getCookie(name))
	document.cookie=name+"="+((path)?"; path="+path:"")+
	((domain)?"; domain="+domain:"")+"; expires=Thu, 01-Jan-70 00:00:01 GMT";
}

function fixDate(date) {
var base=new Date(0);
var skew=base.getTime();
if(skew>0)
	date.setTime(date.getTime()-skew);
}


var checkIntervalDays=30;

function getCheckInterval() {
return checkIntervalDays*24*60*60*1000;
}

function setOwnCookie(cname, cvalue, checkIntervalDays) {
if(getCheckInterval()>0) {
	var expires=new Date();
	fixDate(expires); // NN2/Mac bug
	expires.setTime(expires.getTime()+getCheckInterval());
	setCookie(cname,cvalue,expires,'/')
	}
}


String.prototype.trim=function(){
        return this.replace(/(^\s*)|(\s*$)/g, "");
}
String.prototype.ltrim=function(){
        return this.replace(/(^\s*)/g,"");
}
String.prototype.rtrim=function(){
        return this.replace(/(\s*$)/g,"");
}

function createXMLHttpRequest()
 {
     var xmlHttp;
     try
     {
		//Firefox,Opera 8.0+ safari
		xmlHttp = new XMLHttpRequest();
		xmlHttp.overrideMimeType("text/xml");
     }     
     catch (e)
     {
         //Inter Expplorer
         try
         {
             xmlHttp = new ActiveXObject("Msxm12.XMLHTTP");
         }
         
         catch(e)
         {
             try 
             {
                 xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
             }
             catch (e) 
             {
                 alert("Your browser does not support AJAX!");
                 return false;
             }
         }
     }
     return  xmlHttp;
 }  

function ajax_sendreq(post_data, divID, showresp, param, waitfunc)
{
	var time_out_flag = false;
	var xmlHttp;
	var uri;
	uri = "http://" + document.location.host
	uri += "/cgi-bin/ajax_mgt.cgi";
	var states = new Array("Initiating......", "Initiating request......Finished!<p> Sending request......", "Finished!<p>Receiving data......", "Finished!<p> Processing data, wait :-)", "Completed!");
	xmlHttp = createXMLHttpRequest();
	if(!xmlHttp)
	  return false;
	try {
		xmlHttp.open("POST", uri, true);
	} catch (e) {
		if (window.location.hostname == "localhost") {
			alert("Your browser blocks XMLHttpRequest to 'localhost', try using a real hostname for development/testing.");
		}
		throw e;
	}
	xmlHttp.setRequestHeader("Method", "POST " + uri + " HTTP/1.1");
	xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xmlHttp.onreadystatechange = function()
 
//function filter_get_resp( xmlHttp, states )
{
	var msgDiv;
	msgDiv = document.getElementById(divID)
	if (xmlHttp.readyState != 4)
	{
		//alert(xmlHttp.readyState);
		msgDiv.innerHTML = states[xmlHttp.readyState];
	}
	else if (xmlHttp.status == 200)
	{
		var xmlDoc = xmlHttp.responseXML; //IE
		if (null == xmlDoc) {
			try {//FireFox,Chrome,Safari, xml format is stricter than IE
				var parseXml = new DOMParser();
				var xmlDoc = parseXml.parseFromString(xmlHttp.responseText, "text/xml");
				if (xmlDoc.getElementsByName("parseerror")) {
					var errorMsg = (new XMLSerializer()).serializeToString(xmlDoc);
					msgDiv.innerHTML = errorMsg + xmlHttp.responseText;
					return;
				}
			} catch(e) {
				alert(e.message);
				msgDiv.innerHTML = e.message;
				return;
			}
		}
		if (xmlDoc) {
			//alert("xml string:" + (new XMLSerializer()).serializeToString(xmlDoc));
			var documentElement = xmlDoc.documentElement;
			if (documentElement.tagName == "Tag_ajax") {//for error case!
				msgDiv.innerHTML = documentElement.firstChild.data;
			} else {
				msgDiv.innerHTML = showresp(documentElement, param);
				//msgDiv.innerHTML = "ok";
				//alert(Display(documentElement,1,0,""));
			}
		} else {
			//debug
			//var xmlDocument = xmlHttp.responseText;
			//msgDiv.innerHTML=xmlDocument;
			msgDiv.innerHTML = "Failure";
		}
		clearTimeout(timer); // cancel timer
	} else {
		var error_cause = "";
		if (time_out_flag) {
			error_cause = "Process time out!<p>"
		}
		error_cause += "Error: " + xmlHttp.status + " " + xmlHttp.statusText + " (" + xmlHttp.responseText + ")";
		msgDiv.innerHTML = error_cause;
	}
}

	// start a timer to protect no response after 100 seconds
	// and gateway also has a timer, if it is timeout, it will report error 502 gateway timeout
	var timer = setTimeout(function() {
		time_out_flag = true;
		xmlHttp.abort(); //stop XMLHttpRequest
	}, 5 * 100 * 1000);

	xmlHttp.send(post_data);
	//alert("ajax_sendreq:" + post_data);
	delete xmlHttp;
}
