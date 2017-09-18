function prepareFrame() {
    var ifrm = document.createElement("iframe");
    ifrm.setAttribute("src", "http://google.com/");
    ifrm.style.width = "640px";
    ifrm.style.height = "480px";
    document.body.appendChild(ifrm);
}

function testfunction() {
	alert("why doesn't it show text?");
}

//var button = document.createElement("button");
//document.body.appendChild()