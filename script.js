let processes = [];
let id = 1;

function addProcess() {
    let at = +arrival.value;
    let bt = +burst.value;
    let pr = +priority.value;

    processes.push({id, at, bt, pr});

    let row = table.insertRow();
    row.innerHTML = `<td>P${id}</td><td>${at}</td><td>${bt}</td><td>${pr}</td>`;
    id++;
}

function run() {
    let algo = document.getElementById("algo").value;
    let q = +document.getElementById("quantum").value || 2;

    let arr = JSON.parse(JSON.stringify(processes));
    let time = 0, completed = [], gantt = [];
    let wt = 0, tat = 0;

    if (algo === "fcfs") arr.sort((a,b)=>a.at-b.at);

    while (completed.length < arr.length) {

        let available = arr.filter(p => p.at <= time && !completed.includes(p));

        if (available.length === 0) {
            time++;
            continue;
        }

        let p;

        if (algo === "sjf")
            p = available.sort((a,b)=>a.bt-b.bt)[0];

        else if (algo === "priority")
            p = available.sort((a,b)=>a.pr-b.pr)[0];

        else if (algo === "fcfs")
            p = available[0];

        else break;

        let start = time;
        let end = start + p.bt;

        gantt.push({id:p.id, start, end});

        wt += start - p.at;
        tat += end - p.at;

        time = end;
        completed.push(p);
    }

    // ROUND ROBIN
    if (algo === "rr") {
        let queue = arr.map(p=>({...p}));
        time = 0;

        while(queue.length>0){
            let p = queue.shift();

            if(p.at>time){
                time=p.at;
            }

            let exec = Math.min(q,p.bt);
            let start=time;
            let end=time+exec;

            gantt.push({id:p.id,start,end});

            time=end;
            p.bt-=exec;

            if(p.bt>0) queue.push(p);
            else{
                wt+=start-p.at;
                tat+=end-p.at;
            }
        }
    }

    drawGantt(gantt);

    let avgWT = wt/processes.length;
    let avgTAT = tat/processes.length;
    let cpuUtil = (gantt[gantt.length-1].end / time)*100;

    output.innerText =
    `Avg WT: ${avgWT.toFixed(2)} | Avg TAT: ${avgTAT.toFixed(2)} | CPU Utilization: ${cpuUtil.toFixed(2)}%`;
}

function drawGantt(gantt){
    let g = document.getElementById("gantt");
    let t = document.getElementById("timeline");

    g.innerHTML="";
    t.innerHTML="";

    gantt.forEach(block=>{
        let width = (block.end - block.start)*40;

        let colors = ["#22c55e","#38bdf8","#facc15","#f472b6","#a78bfa"];

g.innerHTML += `
<div class="block" style="
    width:${width}px;
    background:${colors[block.id % colors.length]};
">
P${block.id}
</div>`;
        t.innerHTML += `<div style="width:${width}px">${block.start}</div>`;
    });

    t.innerHTML += `<div>${gantt[gantt.length-1].end}</div>`;
}