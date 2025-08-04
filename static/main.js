

    function alert() {
        Swal.fire({
            title: "Good job!",
            text: "You clicked the button!",
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
    elemSelect.addEventListener("change", function () {
        if (elemSelect.value == "light") {
            document.documentElement.setAttribute("modo-light-dark", "light");
        } else if (elemSelect.value == "dark") {
            document.documentElement.setAttribute("modo-light-dark", "dark");
        }
    });
