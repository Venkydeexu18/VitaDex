const inp =  document.getElementsByClassName("query")[0];
const tags = document.querySelectorAll(".tag");

tags.forEach((tag) => {
    tag.addEventListener("click", () => {
        inp.value = "";
        inp.value = tag.textContent;
    })
})