const monPar = document.getElementsByClassName('incont')[0];
const perPar = document.getElementsByClassName('l-labels')[0];
const cont = document.getElementById('cont');
const hcont = document.getElementById('h-cont');

var months = ['sun','mon','tue','wed','thur','fri'
,'sat']

var percents = ['81% - MAX','61% - 80%','41% - 60%','21% - 40%','0% - 20%'];

var data = [80,40,20,65,75,57,82]



const createNewElem = (cname, arr, parent) => {
    const newElem = document.createElement('div');
    newElem.classList.add(cname);
    newElem.textContent = arr[i];
    parent.appendChild(newElem);
    return newElem;
}


const createnestElem = (pcname, scname, parent, st) => {
    const newElem = document.createElement('div');
    const subElem = document.createElement('div');
    newElem.classList.add(pcname);
    subElem.classList.add(scname);
    newElem.appendChild(subElem);
    if(st){
        let tot = 200;
        let percent = (data[i]/tot) * 100;
        newElem.style.bottom = percent + "%";
    }
    parent.appendChild(newElem);
    return subElem;
}

for(var i=0; i<months.length; i++){
    createNewElem('label',months,monPar);
    let newline = createnestElem('l-cont', 'line', cont, false);
    const d = createnestElem('dot', 'idot', newline, true);
    const h = createNewElem('hover',[],d);
    data[i] = "Glucose : " + data[i];
    const p = createNewElem('hlabel',data,h);
    
}

for(var i=0; i<percents.length; i++){
    createNewElem('l-label',percents,perPar)
    createNewElem('hl-cont',[],hcont)
}
