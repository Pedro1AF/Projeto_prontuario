

    function alert() {
        Swal.fire({
            title: "Paicente adicionado com sucesso!",
            text: "ação concluida!",
            icon: "success"
        });
    }

    function exclu() {
        Swal.fire({
            title: "Paicente deletado com sucesso!",
            text: "ação concluida!",
            icon: "success"
        });
    }


    function checkboxExclusivo(clicked) {
        const checkboxes = document.getElementsByName("sexo");
        checkboxes.forEach((box) => {
            if (box !== clicked) {
                box.checked = false;
            }
        });
    }

const elemSelect = document.querySelector("#selctModo");

// Verifica se há um tema salvo no localStorage ao carregar a página
const temaSalvo = localStorage.getItem("modo-light-dark");
if (temaSalvo) {
    document.documentElement.setAttribute("modo-light-dark", temaSalvo);
    elemSelect.value = temaSalvo; // Atualiza a seleção no <select>
}

// Escuta alterações no select
elemSelect.addEventListener("change", function () {
    const modoSelecionado = elemSelect.value;

    // Aplica o tema e salva no localStorage
    document.documentElement.setAttribute("modo-light-dark", modoSelecionado);
    localStorage.setItem("modo-light-dark", modoSelecionado);
});
