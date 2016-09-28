function loaddef()
{
	uname = getCookie("uname");
	//used for test
	//setOwnCookie(uname+"_filter", "maint", 5)
	if ((uname == null) || (uname == ""))
	{
		alert(Please lonin!);
		window.top.location="../index.html";
		return;
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
	filter_get_req("", "");
}

function get_user_filter()
{
	uname = getCookie("uname");
	if ((uname == null) || (uname == ""))
	{
		alert(Please lonin!);
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
  ajax_sendreq(post_data,filter_get_resp);
}

function filter_get_resp()
	{
		var msgDiv;
	msgDiv = document.getElementById("filter_panel")
	if (xmlHttp.readyState != 4)
	{
		//alert(xmlHttp.readyState);
		msgDiv.innerHTML = states[xmlHttp.readyState];
	}
	else if (xmlHttp.status == 200)
	{
		var xmlDocument = xmlHttp.responseXML;
		//var xmlDocument = xmlHttp.responseText;
		//alert(xmlDocument);
    var documentElement=xmlDocument.documentElement;
   	if(documentElement)
   	{
   		if(documentElement.tagName == "Tag_ajax")//for error case!
   			msgDiv.innerHTML = documentElement.firstChild.data;
   		else
     	  msgDiv.innerHTML = documentElement.firstChild.data;
     	  //alert(Display(documentElement,1,0,""));
    }
    else
     	  msgDiv.innerHTML="failure";
	}
	else 
		msgDiv.innerHTML = "Error: " + xmlHttp.status + " " + xmlHttp.statusText + " (" + xmlHttp.responseText + ")";
}     

