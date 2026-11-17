/* Optional full-screen-style reader for native PreTeXt Learning Intentions. */
(() => {
  "use strict";
  function cleanClone(node){
    const copy=node.cloneNode(true);
    copy.removeAttribute?.("id");
    copy.querySelectorAll?.("[id]").forEach(el=>el.removeAttribute("id"));
    copy.querySelectorAll?.(".autopermalink").forEach(el=>el.remove());
    return copy;
  }
  function init(){
    const blocks=[...document.querySelectorAll("main .objectives, .ptx-content .objectives")];
    if(!blocks.length)return;
    let dialog,heading,label,body,previous,next,counter,close;
    let sentences=[],index=0,trigger=null;
    function makeDialog(){
      if(dialog)return;
      dialog=document.createElement("dialog");
      dialog.className="learning-intentions-dialog";
      dialog.setAttribute("aria-label","Learning Intentions reader");
      dialog.innerHTML=[
        '<div class="li-dialog-head">',
        '<span class="li-dialog-context"></span>',
        '<button type="button" class="li-dialog-close">Close ×</button>',
        '</div>',
        '<div class="li-dialog-body">',
        '<h2>Learning Intentions</h2>',
        '<div class="li-dialog-text" aria-live="polite"></div>',
        '</div>',
        '<div class="li-dialog-foot">',
        '<button type="button" class="li-dialog-previous">← Previous</button>',
        '<span class="li-dialog-counter"></span>',
        '<button type="button" class="li-dialog-next">Next →</button>',
        '</div>'
      ].join("");
      heading=dialog.querySelector(".li-dialog-context");
      body=dialog.querySelector(".li-dialog-text");
      counter=dialog.querySelector(".li-dialog-counter");
      previous=dialog.querySelector(".li-dialog-previous");
      next=dialog.querySelector(".li-dialog-next");
      close=dialog.querySelector(".li-dialog-close");
      previous.addEventListener("click",()=>show(index-1));
      next.addEventListener("click",()=>show(index+1));
      close.addEventListener("click",()=>dialog.close());
      dialog.addEventListener("close",()=>{if(trigger?.isConnected)trigger.focus();});
      dialog.addEventListener("keydown",event=>{
        if(event.ctrlKey||event.altKey||event.metaKey)return;
        if(event.key==="ArrowRight"){event.preventDefault();show(index+1);}
        if(event.key==="ArrowLeft"){event.preventDefault();show(index-1);}
      });
      document.body.appendChild(dialog);
    }
    function show(i){
      index=Math.max(0,Math.min(sentences.length-1,i));
      body.replaceChildren(cleanClone(sentences[index]));
      counter.textContent=(index+1)+" of "+sentences.length;
      previous.disabled=index===0;
      next.disabled=index===sentences.length-1;
      if(window.MathJax?.typesetPromise&&!body.querySelector("mjx-container"))
        window.MathJax.typesetPromise([body]).catch(()=>{});
    }
    for(const block of blocks){
      if(block.dataset.liEnhanced==="yes")continue;
      const h=block.querySelector(".heading,h2,h3,h4");
      if(!h||!h.textContent.includes("Learning Intentions"))continue;
      const items=[...block.querySelectorAll("li")].filter(el=>el.textContent.trim());
      if(!items.length)continue;
      block.dataset.liEnhanced="yes";
      // Keep the presentation control discreet: double-click the intentions.
      function openReader(){
        makeDialog();sentences=items;trigger=block;
        const section=block.parentElement;
        const title=section?.querySelector(":scope > .heading,:scope > h1,:scope > h2,:scope > h3,:scope > h4");
        heading.textContent=(title?.textContent||"Mathematics").trim().replace(/\s+/g," ");
        show(0);dialog.showModal();close.focus();
      }
      block.addEventListener("dblclick",event=>{
        if(event.target.closest("a,button,input,select,textarea"))return;
        event.preventDefault();
        openReader();
      });
      // A keyboard equivalent preserves access without displaying a button.
      block.tabIndex=0;
      block.addEventListener("keydown",event=>{
        if(event.target===block && (event.key==="Enter" || event.key===" ")){
          event.preventDefault();
          openReader();
        }
      });
    }
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});
  else init();
})();