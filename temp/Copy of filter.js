function loaddef()
{
	uname = getCookie("uname");
	//used for test
	//setOwnCookie(uname+"_filter", "maint", 5)
	if ((uname == null) || (uname == ""))
	{
		alert("Please lonin!");
		window.top.location="../index.html";
		return true;
	}
	cur_filter = getCookie(uname+"_filter")
	empty = "";
	if(cur_filter)
	{
		empty = "Current Filter: " + cur_filter;
		empty += "<p><a href='upload.html'>please upload trace</a>"
	}
	else
	{
		get_user_filter();
	}
	filterDiv = document.getElementById("filter_panel")
	filterDiv.innerHTML = empty
}

function upload_file()
{
	content= "<p><a href='upload.html'>please upload trace</a>";
	filterDiv = document.getElementById("filter_panel");
	filterDiv.innerHTML = content;
}

function createfilter(input)
{
	fname = input.elements["fname"].value;
	msgids = input.elements["msgids"].value;
	fmmids = input.elements["fmmids"].value;
	uname = getCookie("uname");
	if(uname)
	{
		if(fname.length==0 || fname.trim()=="")
		{
			alert('Invalid Filter name !');
		  return false;
		}
		if((msgids.length==0 || msgids.trim()=="")
		    && (fmmids.length==0 || fmmids.trim()==""))
		{
				alert("Invalid msgID or fmmID !");
				return false;	
		}
		input.elements["uname"].value = uname
		return true;
	}
	else
	{
				alert("Please login!");
				document.location = "../index.html"
				return false;
	}
}

function get_all_filter()
{
	filter_get_req("");
}

function get_user_filter()
{
	uname = getCookie("uname");
	//alert(uname);
	if ((uname == null) || (uname == ""))
	{
		alert("Please lonin!");
		window.top.location="../index.html";
	}
	else
	{
		filter_get_req(uname);		
	}
}

function filter_get_req(uname)
{
	post_data = "action=getfilter";
	post_data += "&uname=" + uname;
	//alert(post_data);
  ajax_sendreq(post_data, "filter_panel", showfilterlist, null, null);
}

function showfilterlist(de)
{
		if( de.childNodes.length>0)
   {
   	cuname = getCookie("uname");
	if (cuname == null || cuname == "")
	{
				alert("Please login!");
				document.location = "../index.html"
				return;
	}
	version = getCookie(cuname+"_version");
   	showFlag = false;
	if (version == null || version == "")
	{
	    content = "Version not selected! <p>"
	}
	else
	{
	    content = "User: " + cuname + "<p>";
		content += "Version: " + version + "<p>"; 
	}
   	content += "<table border='1'><tr><td>Filter ID</td><td>User Name</td><td>Filter Name</td><td>Msg ID</td><td>FMM ID</td><td>Descriptoin</td></tr>";
   	for(var i=0;i<de.childNodes.length;i++)
    {
      content += "<tr>"
       var child=de.childNodes[i];
       showFlag = false;
       for(var j=0;j<child.childNodes.length;j++)
      {
       var field=child.childNodes[j];
       content += "<td>"
       newName = field.tagName;
       if (newName == "uname")
       {
       	  uname = field.getAttribute("value");
       	  if (cuname == uname)
       	  {
       	     showFlag = true;	
       	  }
       }
       if((newName == "fname") && showFlag)
  		 {
  		    fname = field.getAttribute("value");
  		    content += "<a href='javascript:reservefilter(\"" + fname + "\");'>" + fname + "</a>";
  		 }
  		 else
  		 {
  		 	  content += field.getAttribute("value");
  		 }
  		 content += "</td>"
  		} 
  	  content += "</tr>"		 
		}
		content += "</table>"
  	//alert(content);
  	return content; 
	}
	else
	{
	    return 'No filter created!';
	}	
}

function reservefilter(fname)
{
   setOwnCookie(uname+"_filter", fname, 5)
   location.reload();
}

function handle_setversion(input)
{
    version = input.elements["rel"].value;
    //alert(version);
	//used for test
	uname = getCookie("uname");
	//alert(uname);
	if ((uname == null) || (uname == ""))
	{
		alert("Please lonin!");
		window.top.location="../index.html";
	}
	else
	{
	    setOwnCookie(uname+"_version", version, 5)
	}
}

function showver_proxy(de, param)
{
    if( de.childNodes.length>0)
    {
	    content = "<form method=get onsubmit=\"return handle_setversion(this);\">"
		content += "<select name=rel>"
        for(var i=0;i<de.childNodes.length;i++)
        {
	        var child=de.childNodes[i];
            newName = child.tagName;
            content += "<option value=" + newName + " > Release " +newName
        }
        content += "</select><p>"
        content += "<input type=submit value=Set_Version>"
        content += "<input type=reset value=Reset><p>"
        content += "</form>"
	}
	//alert(content)
	return content
}

function setversion()
{
  post_data = "action=listbscversion";
  //alert(post_data);
  ajax_sendreq(post_data, "filter_panel", showver_proxy, null, null);
}

function showbuffer()
{
	cuname = getCookie("uname");
	if (cuname == null || cuname == "")
	{
				alert("Please login!");
				parent.location = "../index.html"
				return;
	}
	version = getCookie(cuname+"_version");
	if (version == null || version == "")
	{
	    content = "Version not selected! <p>"
		filterDiv = document.getElementById("filter_panel");
	    filterDiv.innerHTML = content;
		return;
	}
	post_data = "action=showbuffer";
	post_data += "&version="+version;
	//alert(post_data);
  ajax_sendreq(post_data, "filter_panel", disbuffer, null, null);
}

function disbuffer(de, param)
{
	//alert('disbuffer');	
	if( de.childNodes.length>0)
   {
   cuname = getCookie("uname");
	if (cuname == null || cuname == "")
	{
				alert("Please login!");
				document.location = "../index.html"
				return;
	}
	version = getCookie(cuname+"_version");
	if (version == null || version == "")
	{
	    content = "Version not selected! <p>"
	}
	else
	{
	    content = "User: " + cuname + "<p>";
		content += "Version: " + version + "<p>"; 
	}
   	content += "<table border='1'><tr><td>Message ID</td><td>User Buffer</td><td>Action</td></tr>";
   	for(var i=0;i<de.childNodes.length;i++)
    {
      content += "<tr>";
       var child=de.childNodes[i];
       content += "<td>";
       newName = child.tagName;
       msgID = newName.substring(4);
       content += msgID + "</td><td>"
       if(child.getAttribute("value"))
        	content += child.getAttribute("value") + "</td><td>";
       else
        	content += "</td><td>";
        content += "<a href='javascript:editbuffer(\"" + msgID + "\", \"filter_panel\");'>Edit</a>";
  	  content += "</tr>"		 
		}
		content += "</table>"
  	//alert(content);
  	return content; 
	}
	else
	{
	    return 'No msg with buffer!';
	}	
}

function editbuffer(msgid, divID)
{
	cuname = getCookie("uname");
	if (cuname == null || cuname == "")
	{
				alert("Please login!");
				parent.location = "../index.html"
				return;
	}
	version = getCookie(cuname+"_version");
	if (version == null || version == "")
	{
	    content = "Version not selected! <p>"
		filterDiv = document.getElementById("filter_panel");
	    filterDiv.innerHTML = content;
		return;
	}
	post_data = "action=listbuffer";
	post_data += "&version="+version;
	//alert(post_data);
	param = msgid;
  ajax_sendreq(post_data, divID, listallbuffer, param, null);	
}

function listallbuffer(de, param)
{
	if( de.childNodes.length>0)
   {
   	msgID = param;
   	content = "Select User Buffer Mode for msg " + msgID + ":<p>";
   	content += "<form name='setbuffer'>"
	  content += "<select name='selectbuffer' onchange='setubuffer(\"" + msgID + "\")'>";
   	for(var i=0;i<de.childNodes.length;i++)
    {      
       var child=de.childNodes[i];
       newName = child.tagName;
       content += "<option value =\"" + newName + "\">" + newName + "</option>";       		 
		}
		content += "</select></form>";
  	//alert(content);
  	return content; 
	}
	else
	{
	    return 'No buffer mode defined!';
	}	
}

function setubuffer(msgid)
{
	cuname = getCookie("uname");
	if (cuname == null || cuname == "")
	{
				alert("Please login!");
				parent.location = "../index.html"
				return;
	}
	version = getCookie(cuname+"_version");
	if (version == null || version == "")
	{
	    content = "Version not selected! <p>"
		filterDiv = document.getElementById("filter_panel");
	    filterDiv.innerHTML = content;
		return;
	}
	var i=document.setbuffer.selectbuffer.selectedIndex;  
  var buffermode=document.setbuffer.selectbuffer.options[i].value;
  post_data = "action=setbuffer";
  post_data += "&msgid=" + msgid;
  post_data += "&mode=" + buffermode;
  post_data += "&version="+version;
	//alert(post_data);
  ajax_sendreq(post_data, "filter_panel", showbuffer, null, null); 	
}

function select_mode()
{
	filterDiv = document.getElementById("editmode");
	filterDiv.innerHTML = 'You can select mode here.<P>Comming soon...';
}