async function login(){
    let u=u.value,p=p.value;

    let r=await fetch("/api/login",{method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({username:u,password:p})});

    if(r.ok) location="/dashboard";
    else alert("fail");
}

async function register(){
    let u=u.value,p=p.value;

    await fetch("/api/register",{method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({username:u,password:p})});

    location="/login";
}

async function getData(){
    let s=state.value;

    let r=await fetch("/api/predict",{method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({state:s})});

    let d=await r.json();

    let html="";
    d.top5.forEach(x=>{
        html+=`<p>${x.crop} ₹${x.profit}</p>`;
    });

    html+=`<h2>Best: ${d.best.crop}</h2>`;
    html+=`<h3>Mandi: ${d.mandi.market}</h3>`;

    output.innerHTML=html;
}