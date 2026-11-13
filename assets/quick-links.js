/* Unobtrusive ABCD shortcuts, deliberately separate from the book's logo.
   The original PreTeXt brandlogo continues to link to the book's home. */
(()=>{
 "use strict";
 if(document.querySelector(".book-abcd-quick-links"))return;
 const css=document.createElement("link");
 css.rel="stylesheet";
 css.href="quick-links.css?v=1";
 document.head.append(css);
 const nav=document.createElement("nav");
 nav.className="book-abcd-quick-links";
 nav.setAttribute("aria-label","Quick links: A Apps, B Book, C Calculator, D Desmos");
 const links=[
  ["red","A · Apps","https://ronandownes.github.io/maths/"],
  ["green","B · Maths Book","https://ronandownes.github.io/book/"],
  ["blue","C · Calculator","https://ronandownes.github.io/calculator/"],
  ["black","D · Desmos","https://www.desmos.com/calculator"]
 ];
 for(const [colour,label,href] of links){
   const a=document.createElement("a");
   a.className="book-abcd-"+colour;
   a.href=href;a.title=label;
   a.setAttribute("aria-label",label);
   if(colour==="black"){a.target="_blank";a.rel="noopener noreferrer";}
   const dot=document.createElement("i");dot.setAttribute("aria-hidden","true");
   a.append(dot);nav.append(a);
 }
 // PreTeXt supplies its own toolbar for contents, search and navigation.
 // Append small shortcuts to that toolbar without modifying its logo.
 const toolbar=document.querySelector(".ptx-navbar,.ptx-toolbar,.ptx-navbar-global,.ptx-page-navbar");
 if(toolbar){
   toolbar.append(nav);
 }else{
   const masthead=document.querySelector(".ptx-banner,header#masthead,header");
   if(masthead)masthead.insertAdjacentElement("afterend",nav);
   else document.body.prepend(nav);
   nav.classList.add("book-abcd-standalone");
 }
})();