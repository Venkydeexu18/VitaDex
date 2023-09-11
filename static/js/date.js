const date = Date().split(" ")
const weeks = ['sun','mon','tue','wed','thur','fri','sat'];
let apppointment = 16;
const dcont = document.getElementsByClassName("dcont")[0]

for (i=0; i<7; i++){
    let d = parseInt(date[2]) + i;let mon = date[1];let yr = date[3]
    let dy = new Date(`${mon} ${d}, ${yr}`);
    let w = dy.getDay();

    const cont = document.createElement("div")
    const wd = document.createElement("div")
    const day = document.createElement("div")
    
    cont.classList.add("datecont")   
    apppointment === d ? cont.classList.add("sel") : null
    wd.classList.add("w")
    day.classList.add("d")

    wd.textContent = weeks[w]
    day.textContent = d

    cont.appendChild(wd)
    cont.appendChild(day)
    dcont.appendChild(cont)
}
