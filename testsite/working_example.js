window.onload = function (_) {
var t1=document.createElement("p");t1.innerHTML="H";var i1=new FontFace("I1","url(test1.woff2)");i1.load().then(function(face){document.fonts.add(face);t1.style.fontFamily=face.family;document.body.appendChild(t1);});
var t2=document.createElement("p");t2.innerHTML="H";var i2=new FontFace("I2","url(test2.woff2)");i2.load().then(function(face){document.fonts.add(face);t2.style.fontFamily=face.family;document.body.appendChild(t2);});
};




