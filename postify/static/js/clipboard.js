function copyToClipboard(button){
    console.log("clicked");
    const copy_text = button.innerHTML;
    navigator.clipboard.writeText(copy_text).then(()=>{
        alert(`${copy_text} Copied`);
    });
}

const copyButtons = document.querySelectorAll(".copy");

copyButtons.forEach( button => {
    button.addEventListener("click",function (){
        copyToClipboard(button = button);
    });
});
