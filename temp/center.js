
function showFmm(content)
{
	window.status = content	
}

function showRaw(content)
{
	msg = content
	if(content && content.length > 0 && content.indexOf("$") != -1)
	{
		msgs = content.split("$")
		msg = ""
		for(i=0;i<msgs.length;i++)
		{
			msg	+= msgs[i] + "<p>"
		}	
	}
	msgDiv = document.getElementById("msgPanel")
	msgDiv.innerHTML = msg
}

function clearMsg()
{
	//empty = "Show msg content"
	//msgDiv = document.getElementById("msgPanel")
	//msgDiv.innerHTML = empty
}

function showDetailedMsg(msg_content)
{
	var xmlHttp;
	var uri;
	var post_data;
	cuname = getCookie("uname");
	if (cuname == null || cuname == "")
	{
				alert("Please login!");
				window.top.location = "../index.html"
				return;
	}
	version = getCookie(cuname+"_version");
	if (version == null || version == "")
	{
	    content = "Version not selected! <p>";
		div_tag = document.getElementById('msgPanel');
        div_tag.innerHTML = content;
		return;
	}
	uri = "http://" + document.location.host
	uri += "/cgi-bin/ajax_mgt.cgi";
	post_data = "action=decodemsg&msg=" + msg_content;
	post_data += "&version="+version;
	ajax_sendreq(post_data, "msgPanel", showmsg_proxy, null, null);
}

function loadSvg()
{
	svg_curr_index = getCookie("svg_curr_index");
	svg_num = getCookie("svg_num");
	svg_fname = getCookie("svg_file_name");
	svgwidth = getCookie("svg_width");
	svgheight = getCookie("svg_height");
  
	if (svg_num && svg_fname && svgwidth && svgheight)
	//if(1)
	{
		svgContent = "";
		if(svg_num > 1)
		{
			if(svg_curr_index)
			{
				if(svg_curr_index > 0)
					svgContent += "<a href='#' LANGUAGE=javascript onclick='page_nevigate(true)'><-prev</a>";
				svgContent += "&nbsp&nbsp";
				if(svg_curr_index < svg_num-1)
					svgContent += "<a href='#' LANGUAGE=javascript onclick='page_nevigate(false)'>next-></a>";
			}
			else
			{
				svg_curr_index = 0;
				setOwnCookie("svg_curr_index", svg_curr_index, 1);
				svgContent += "&nbsp&nbsp";
				svgContent += "<a href='#' LANGUAGE=javascript onclick='page_nevigate(false)'>next-></a>";
			}
			svgContent += "&nbsp&nbsp";
			svgContent += String(Number(svg_curr_index) +1) + "/" + svg_num + "<p>";
		}
		else
			svg_curr_index = 0;
		//alert(svg_curr_index);
		svg_fname = svg_fname.split(";")[svg_curr_index];
		//alert(svg_fname);
		svgwidth = svgwidth.split(";")[svg_curr_index];
		//alert(svgwidth);
		svgheight = svgheight.split(";")[svg_curr_index];
		//alert(svgheight);
		svgContent += '<embed src="' + svg_fname;
		svgContent += '" width="' + svgwidth;
		svgContent += '" height="' + svgheight;
		svgContent += '" type="image/svg+xml" pluginspage="http://www.adobe.com/svg/viewer/install/" /><p>';
		if(svg_num > 1)
		{
			if(svg_curr_index)
			{
				if(svg_curr_index > 0)
					svgContent += "<a href='#' LANGUAGE=javascript onclick='page_nevigate(true)'><-prev</a>";
				svgContent += "&nbsp&nbsp";
				if(svg_curr_index < svg_num-1)
					svgContent += "<a href='#' LANGUAGE=javascript onclick='page_nevigate(false)'>next-></a>";
			}
			else
			{
				svg_curr_index = 0;
				setOwnCookie("svg_curr_index", svg_curr_index, 1);
				svgContent += "&nbsp&nbsp";
				svgContent += "<a href='#' LANGUAGE=javascript onclick='page_nevigate(false)'>next-></a>";
			}
			svgContent += "&nbsp&nbsp";
			svgContent += String(Number(svg_curr_index) +1) + "/" + svg_num + "<p>";
		}
	}
	else
	{
		alert("Please upload trace file");
		return;
	}
	//svgContent = '<embed src="../trace/20100421_074648_20100421_075432_1.3.6_SCPR_[1]_1014.rtrc_backup.out.svg" width="6670" height="11820" type="image/svg+xml" pluginspage="http://172.24.178.26/SVGView.exe" />';
	//alert(svgContent);
	svgDiv = document.getElementById("svgdiv");
	svgDiv.innerHTML = svgContent;
	//alert(window.location);
}

function page_nevigate(flag)
{
	svg_curr_index = Number(getCookie("svg_curr_index"));
	if(flag)
		svg_curr_index -= 1;
	else
		svg_curr_index += 1;
	setOwnCookie("svg_curr_index", svg_curr_index, 1);
	loadSvg();	
}

function decode_single_msg()
{
	var msg_content = document.getElementById("msgcontent").value;
	//alert(msg_content);
	if (!msg_content || msg_content == "") {
		alert("Message is empty!");
		return;
	}
	var obj = document.getElementById('version');
	var index = obj.selectedIndex; 
	var version = obj.options[index].value;
	if (version == null || version == "")
	{
		alert("Version not selected! Please select Version.");
		return;
	}
	post_data = "action=decodesinglemsg";
	post_data += "&msgcontent=" + msg_content;
	post_data += "&uname=" + getCookie("uname");
	post_data += "&version=" + version;
	post_data += "&objname=" + document.getElementById("objname").value;
	post_data += "&buffermode=" + document.getElementById("buffermode").value;
	post_data += "&fieldmode=" + document.getElementById("fieldmode").value;
	//alert(post_data);
	ajax_sendreq(post_data, "showmsg", showmsg_proxy, null, null); 	
}

function showmsg_proxy(de, param)
{
	var common = "";
	var title = '<div id="tab_t">';
	var content = '<div id="tab_c">'
	var tab_index = 0;
	for (var i = 0; i < de.childNodes.length; i++) {
		var child = de.childNodes[i];
		if (child.tagName == "chill_list") {
			title += '<li class="normal" onclick="tabs(this,' + tab_index +');">chill list</li>';
			content += '<div id="tab_content' + tab_index + '" style="display:none;">' 
				+ Display(child, i, 0, "", 0) + '</div>';
			tab_index++;
		} else if (child.tagName == "stan") {
			title += '<li class="active" onclick="tabs(this,' + tab_index +');">stan</li>';
			content += '<div id="tab_content' + tab_index + '" style="display:block;">' 
				+ DisplayXmlGdb(child, i) + '</div>';
			tab_index++;
		} else {
			common += Display(child, i, 0, "", 0);
		}
	}
	title += '</div>';
	content += '</div>';
	return common + title + content;
}

function clear_div(divID)
{
    div_tag = document.getElementById(divID);
    div_tag.innerHTML = "";
}

function DisplayXmlGdb(node, id)
{
    var ret = "";
    for(var i = 0; i < node.childNodes.length; i++)
    {
        var child = node.childNodes[i];
        if (child.getAttribute("data")) {
            ret += "<div><span>" + child.tagName + "&nbsp;</span><span style=\"color: #9900cc\">" 
                + child.getAttribute("data") + "</span></div>";
        }
        if (child.getAttribute("result")) {
            var result = showXmlGdb(child.getAttribute("result"), id + "_" + i).outerHTML;
            ret += "<div><span>" + (result || child.getAttribute("result")) + "</span></div>";
        }
        ret += "<br/>";
    }
    return ret;
}



// Display(de, 1, 0, "", 0);
function Display(documentElement, n, gDiv, nblack, flag)
{
	var a = "";
	var divSingle = "div" + n;
	if (documentElement.childNodes.length > 0)
	{
		gDiv = gDiv + 1;
		a = a + "<div name=" + gDiv + "_" + flag + ">"; // <div name=1_0>
		var tmp_flag = flag;
		for (var i = 0; i < documentElement.childNodes.length; i++)
		{
			var child = documentElement.childNodes[i];
			newName = child.tagName;
			if (child.tagName.indexOf(".") != -1)
			{
				nameArray = child.tagName.split(".");
				len = nameArray.length;
				newName = nameArray[len - 1];
			}
			if (newName == "NULL") // end point
			{
				newName = "--"
			}
			newName = nblack + newName;
			if (child.childNodes.length > 0)
			{
				var temp = gDiv + 1;
				var spanId = "s" + gDiv;
				spanId += tmp_flag;
				a = a + "<div id=" + divSingle + ">           <span >" + newName 
					+ "                       </span>    <span style=\"color: #3300ff\">" 
					+ child.getAttribute("type") + "</span> <span                        id=" 
					+ spanId + " style='color: #ff0000; cursor:hand' onclick='Expand(" 
					+ temp + "," + tmp_flag + ")'>-</span></div>";
				//alert(a);
				a = a + Display(child, n + 1, gDiv, nblack + "&nbsp&nbsp&nbsp&nbsp", tmp_flag);
			}
			else // end child
			{
				if (child.getAttribute("type"))
				{
					if (child.getAttribute("value"))
					{
						a= a + "<div id=" + divSingle + "><span >" + newName 
							+ "                       </span>    <span style=\"color: #3300ff\">" 
							+ child.getAttribute("type") + "</span>     <span style=\"color: #9900cc\"> " 
							+ child.getAttribute("value") + "</span></div>";
					}
					else
					{
						a = a + "<div id=" + divSingle+"><span >" + newName 
							+ "                       </span>    <span style=\"color: #3300ff\">" 
							+ child.getAttribute("type") + "</span></div>";
					}
				}
				else
				{
					if (child.getAttribute("value"))
					{
						a = a + "<div id=" + divSingle + "><span >" + newName 
							+ "                       </span>     <span style=\"color: #9900cc\"> " 
							+ child.getAttribute("value") + "</span></div>";
					}
					else
					{
						a = a + "<div id=" + divSingle + "><span >" + newName 
							+ "                       </span>    </div>";
					}
				}
			}
			tmp_flag += 1;
		}
		//if(documentElement.getAttribute("type")=="union")
		a = a + '</div>';
		return a;
	}
}

  function Expand(divAll, flag)
 {
       var spanId="s"+(divAll-1);
       spanId += flag;
       divName = ""
       divName += divAll + "_" + flag;
       var s=document.getElementById(spanId);
       var vs =document.getElementsByTagName("div");
       for(i=0;i<vs.length;i++)
       {
       	v = vs[i];
       	if(v.getAttribute("name")==divName)
       	{
         	if(v.style.display=='none')
         	{
         		v.style.display='block';
         		s.innerText="-";
         	}
         	else
         	{
         		v.style.display='none';
         		s.innerText="+";
          }
         }
       }
 }
 
 
 
 
 
function showprogress( filename )
{
	uname = getCookie("uname");
	fname = getCookie(uname+"_filter");
	if (uname == null || uname == "")
	{
		alert("please login");
		//target = "_top";
		window.top.location = "../index.html";
		return;
		}
	if (fname == null || fname == "")
	{
		alert("please select filter");
		//location.target = "_top";
		window.top.location = "../temp/mainframe.html";
		return;
		}
	version = getCookie(uname+"_version");
	if (version == null || version == "")
	{
	    alert("Version not selected! <p>");
		window.top.location = "../temp/mainframe.html";
		return;
	}
	//setInterval(updateprogress,1000);
	post_data = "action=parsetrace&filename=" + filename;
	post_data += "&uname=" + uname;
	post_data += "&fname=" + fname;
	post_data += "&version=" + version;
	//alert(post_data);
	ajax_sendreq(post_data, "prog", preshow, null, null);
}

function updateprogress()
{
  //uploadStr = '	<form enctype="multipart/form-data"  action="save_file.cgi" method="post">   <p>File: <input type="file" name="filename" /></p>    <p><input type="submit" value="Upload" /></p>    </form>';
	progDiv = document.getElementById("prog");
	progDiv.innerHTML = "123";	
}
	
function preshow(de, param)
{
	if( de.childNodes.length==2)
	{
		svg_num = de.childNodes[0].getAttribute("value");
		svg_list = de.childNodes[1];
		if(svg_num != svg_list.childNodes.length)
		{
			return "Parse trace error: svg file number error.";
		}
		//alert("svg_num " + svg_num);
		setOwnCookie("svg_num", svg_num, 1);
		var filename="";
		var swidth="";
		var sheight="";
		for(var i=0;i<svg_list.childNodes.length;i++)
		{
			var child=svg_list.childNodes[i];
			for(var j=0;j<child.childNodes.length;j++)
			{
				var svg_file = child.childNodes[j];
				newName = svg_file.tagName;
  		 		if(newName == "svg_file_name")
  		 		{
  		 			  filename += svg_file.getAttribute("value") + ";";
  		 		}
  		 		if(newName == "svg_width")
  		 		{
  		 				swidth += svg_file.getAttribute("value") + ";";
  		 		}
  		 		if(newName == "svg_height")
  		 		{
  		 				sheight += svg_file.getAttribute("value") + ";";
  		 		}
			}
  		}
  		setOwnCookie("svg_curr_index", "0", 1);
  		//alert("svg_file_name " + filename);
  		setOwnCookie("svg_file_name", filename, 1);
  		//alert("svg_width " + swidth);
  		setOwnCookie("svg_width", swidth, 1);
  		//alert("svg_height " + sheight);
  		setOwnCookie("svg_height", sheight, 1);
  		//alert("redirect..");
  		location = "../temp/center.html"
	}
	else
	{
		return "Parse trace error: parameter number error.";	
	}
}

function load_singlemsg_def()
{
	var version_select = document.getElementById("version");
	var options = [
		'B12_MX_MR2_ED4(AL31)',
		'B12_MX_MR2_ED3(AL09)',
		'B12_MX_MR2_ED1.5(AL06)',
		'B12_MX_MR1_ED2(AL04)',
		'B11_MX_MR3_ED2', 
		'B11_MX_MR3_ED1',
		'B11_MX_MR1_ED2',
		'B12_MR2_ED2',
		'B12_MR1',
		'B12_MR1_ED0',
		'B12_MR2_ED1',
		'B12_IROPTN',
		'B12_350BTS',
		'B13_MR1 D1'];
	for (var i = 0; i < options.length; i++)
	{
		version_select.options.add(new Option("Release " + options[i], options[i]));
	}

	// set default value
	var cuname = getCookie("uname");
	var version_selected = getCookie(cuname + "_version");
	for (var i = 0; i < version_select.options.length; i++)
	{
		if (version_select.options[i].text == version_selected)
		{
			version_select.options[i].selected = true;
			break;
		}
	}
	if (i == version_select.options.length)
	{
		version_select.options[0].selected = true;
	}
	//cuname = getCookie("uname");
	//version = getCookie(cuname + "_version");
	//if (version == null || version == "")
	//{
	//    content = "Version not selected! <p>"
	//}
	//else
	//{
	//    content = "User: " + cuname + "<p>";
	//	content += "Version: " + version + "<p>";
	//}
	//var msgDiv;
	//msgDiv = document.getElementById("user_panel")
	//msgDiv.innerHTML = content
}

function example1()
{
	var text = "0010367302 09:41:55:837 vostask.c 1100 IMRV:1A 01 00 28 20 4D EA 00 01 00 10 00 01 00 2C 00 01 00 68 29 0A 09 EC 00 01 00 1D 00 0A 00 00 00 01 00 44 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n"
		+ "0010367303 09:41:55:837 vostask.c 1103 IMRV:07 40 01 01 01 01 00 00 00 01 01 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 2B 04 01 00 03 02 00 01 01 01 3C 00 01 00 FF FF 03 03 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 01 0F 0F FF FF 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 0A 04 00 FF DC 07 04 13 09 29 37 08 11 FF FF 01 01 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF\n"
		+ "0010367304 09:41:55:837 vostask.c 1140 IMRV:VCE 1 msg 234 FMM82->FMM8\n";
	document.getElementById("msgcontent").value = text;
	document.getElementById("objname").value = "BTS_EXT_RED.o";
	document.getElementById("buffermode").value = "M_OUTPUT_OPR";
	document.getElementById("fieldmode").value = "T_MSG_0234_MODE"
}

function example2()
{
	var text = "386122182 08:30:20:598 cmw-api.c 1085 EMRV:msg 685 Prio 3 VCE3 FMM49 -> VCE1 FMM4\n"
		+ "386122183 08:30:20:598 cmw-common.c 558 DBUG:Hdr: AA 00 00 00 01 00 00 00 \n"
		+ "					       0: A2 00 03 00 20 3D AD 02  01 00 04 00 03 00 31 00 \n"
		+ "					      16: 01 00 03 00 31 00 00 00  CC 00 00 00 00 00 00 00 \n"
		+ "					      32: 1E 00 00 00 76 00 00 00  94 00 00 00 46 00 30 00 \n"
		+ "					      48: 00 00 00 00 00 00 0F 00  0C 00 00 00 03 00 00 01 \n"
		+ "					      64: FF FF FF FF 00 00 00 00  06 00 00 00 00 01 21 00 \n"
		+ "					      80: 9B 00 FF 0F 02 FF 1B 02  00 00 D2 00 FF FF 00 00 \n"
		+ "					      96: 00 01 C0 00 04 00 FF 00  FF FF 00 00 FF 00 FF FF \n"
		+ "					     112: FF FF FF 00 FF FF 00 00  FF FF 00 00 FF FF 00 00 \n";
	document.getElementById("msgcontent").value = text;
	document.getElementById("objname").value = "REMOTE_REQUEST_HDLR.o";
	document.getElementById("buffermode").value = "ZM_REM_REQ_BUF";
	document.getElementById("fieldmode").value = ""
}

function example3()
{
	// for paper test
	var text = "2619832477 17:22:55:640 cmw-api.c 870 EMSD:msg 541 Prio 1 VCE2 FMM53 -> VCE26 FMM107\n"
		+ "2619832478 17:22:55:640 cmw-common.c 563 DBUG:Hdr: 1E 00 00 00 1A 00 00 00 \n"
		+ "					       0: 16 00 00 06 00 1D 1D 02  1A 00 6B 00 02 00 35 00 \n"
		+ "					      16: 02 00 03 00 00 00 \n";
	document.getElementById("msgcontent").value = text;
	document.getElementById("objname").value = "";
	document.getElementById("buffermode").value = "";
	document.getElementById("fieldmode").value = ""
}

