const API_URL = "";

function getToken() {
    return localStorage.getItem("tiss_token");
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", senha);

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (!res.ok) throw new Error("Credenciais inválidas");

        const data = await res.json();
        localStorage.setItem("tiss_token", data.access_token);
        localStorage.setItem("tiss_user", email);

        iniciarDashboard();
    } catch (err) {
        const errEl = document.getElementById("loginError");
        errEl.innerText = err.message;
        errEl.classList.remove("hidden");
    }
}

function iniciarDashboard() {
    const token = getToken();
    if (!token) return;

    document.getElementById("loginSection").classList.add("hidden");
    document.getElementById("dashboardSection").classList.remove("hidden");
    document.getElementById("userInfo").classList.remove("hidden");
    document.getElementById("userEmail").innerText = localStorage.getItem("tiss_user");

    carregarSolicitacoes();
}

function logout() {
    localStorage.clear();
    window.location.reload();
}

async function carregarSolicitacoes() {
    try {
        const res = await fetch(`${API_URL}/solicitacoes/`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        if (!res.ok) return;

        const solicitacoes = await res.json();
        const tbody = document.getElementById("tabelaSolBody");
        tbody.innerHTML = "";

        solicitacoes.forEach(s => {
            let statusBadge = "";
            if (s.status === "autorizada") {
                statusBadge = `<span class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-semibold">Autorizada</span>`;
            } else if (s.status === "negada") {
                statusBadge = `<span class="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-xs font-semibold">Negada</span>`;
            } else {
                statusBadge = `<span class="bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full text-xs font-semibold animate-pulse">Pendente (RPA)</span>`;
            }

            tbody.innerHTML += `
                <tr class="hover:bg-slate-50">
                    <td class="p-3 font-medium">#${s.id}</td>
                    <td class="p-3">${s.clinica_id}</td>
                    <td class="p-3">${s.paciente_id}</td>
                    <td class="p-3">${s.procedimento}</td>
                    <td class="p-3">${statusBadge}</td>
                    <td class="p-3 text-center">
                        <button onclick="downloadXML(${s.id})" class="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-600 border border-indigo-200 px-2.5 py-1 rounded transition">
                            📄 Download XML
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error("Erro ao carregar solicitações:", err);
    }
}

async function handleNovaSolicitacao(e) {
    e.preventDefault();
    const clinica_id = parseInt(document.getElementById("solClinicaId").value);
    const paciente_id = parseInt(document.getElementById("solPacienteId").value);
    const procedimento = document.getElementById("solProcedimento").value;

    const res = await fetch(`${API_URL}/solicitacoes/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ clinica_id, paciente_id, procedimento })
    });

    if (res.ok) {
        document.getElementById("solProcedimento").value = "";
        carregarSolicitacoes();
    } else {
        alert("Erro ao criar solicitação. Verifique se a clínica e paciente existem.");
    }
}

async function handleValidarXML(e) {
    e.preventDefault();
    const fileInput = document.getElementById("xmlFile");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const resEl = document.getElementById("xmlResult");

    const res = await fetch(`${API_URL}/solicitacoes/validar-xml`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${getToken()}` },
        body: formData
    });

    const data = await res.json();
    resEl.classList.remove("hidden");

    if (res.ok) {
        resEl.className = "mt-3 text-xs p-2.5 rounded bg-green-100 text-green-800 border border-green-200";
        resEl.innerText = `✅ ${data.mensagem}`;
    } else {
        resEl.className = "mt-3 text-xs p-2.5 rounded bg-red-100 text-red-800 border border-red-200";
        resEl.innerText = `❌ ${data.detail?.erro || "Erro na validação do XML"}`;
    }
}

async function downloadXML(id) {
    const res = await fetch(`${API_URL}/solicitacoes/${id}/xml`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
    });
    if (!res.ok) return alert("Erro ao baixar o XML");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `guia_tiss_${id}.xml`;
    document.body.appendChild(a);
    a.click();
    a.remove();
}

// Auto-inicializa se já tiver logado
if (getToken()) {
    iniciarDashboard();
}