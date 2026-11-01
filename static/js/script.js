// ===============================
// DOM ELEMENTS
// ===============================

const uploadBtn = document.getElementById("uploadBtn");
const sendBtn = document.getElementById("sendBtn");
const summaryBtn = document.getElementById("summaryBtn");
const insightsBtn = document.getElementById("insightsBtn");
const clearBtn = document.getElementById("clearBtn");

const pdfFile = document.getElementById("pdfFile");
const question = document.getElementById("question");
const chatWindow = document.getElementById("chatWindow");

// ===============================
// SESSION
// ===============================

let sessionId = null;

// ===============================
// AUTO CREATE SESSION
// ===============================

window.onload = async () => {

    await createSession();

};

// ===============================
// CREATE SESSION
// ===============================

async function createSession(){

    try{

        const response = await fetch("/session");

        const data = await response.json();

        sessionId = data.session_id;

        console.log(sessionId);

    }

    catch(error){

        alert("Unable to create session.");

    }

}

// ===============================
// UPLOAD PDF
// ===============================

uploadBtn.addEventListener(

"click",

async ()=>{

    if(!pdfFile.files.length){

        alert("Please choose PDF.");

        return;

    }

    const formData = new FormData();

    formData.append(

        "report",

        pdfFile.files[0]

    );

    formData.append(

        "session_id",

        sessionId

    );

    try{

        const response = await fetch(

            "/upload",

            {

                method:"POST",

                body:formData

            }

        );

        const data = await response.json();

        addAIMessage(

            "Report uploaded successfully."

        );

    }

    catch(error){

        addAIMessage(

            "Upload failed."

        );

    }

});

// ===============================
// SEND MESSAGE / Chat Function
// ===============================

sendBtn.addEventListener(

"click",

async ()=>{

    const text = question.value.trim();

    if(text==="") return;

    addUserMessage(text);

    question.value="";

    try{

        const response = await fetch(

            "/chat",

            {

                method:"POST",

                headers:{

                    "Content-Type":

                    "application/json"

                },

                body:JSON.stringify({

                    session_id:sessionId,

                    question:text

                })

            }

        );

        const data = await response.json();

        addAIMessage(

            data.answer

        );

    }

    catch(error){

        addAIMessage(

            "Something went wrong."

        );

    }

});

// ===============================
// Summary Button
// ===============================

summaryBtn.addEventListener(

"click",

async()=>{

    const response=await fetch("/summary?session_id=" + sessionId);

    const data=await response.json();

    addAIMessage(data.summary);

});

// ===============================
// Insights Button
// ===============================

insightsBtn.addEventListener(

"click",

async()=>{

    const response=await fetch("/insights?session_id=" + sessionId);

    const data=await response.json();

    addAIMessage(data.insights);

});

// ===============================
// Clear Button
// ===============================

clearBtn.addEventListener(

"click",

async()=>{

    await fetch("/clear?session_id=" + sessionId);

    chatWindow.innerHTML="";

});

// ===============================
// User Bubble
// ===============================

function addUserMessage(message){

    const div=document.createElement("div");

    div.className="user-message";

    div.innerText=message;

    chatWindow.appendChild(div);

    chatWindow.scrollTop=

    chatWindow.scrollHeight;

}

// ===============================
// AI Bubble
// ===============================

function addAIMessage(message){

    const div=document.createElement("div");

    div.className="ai-message";

    div.innerText=message;

    chatWindow.appendChild(div);

    chatWindow.scrollTop=

    chatWindow.scrollHeight;

}