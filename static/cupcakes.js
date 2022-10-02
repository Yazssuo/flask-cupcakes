const API_URL = "http://127.0.0.1:5000/api/cupcakes";

function genCupcakeLi(cupcake) {
    return `
        <div data-c-id=${cupcake.id}>
            <li>
            ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
            <button id="delete-button">X</button>
            </li>
            <img class="Cupcake-img"
                src="${cupcake.image}"
                alt="(no image provided)">
        </div>
    `
};

async function initCupcakes() {
    const response = await axios.get(`${API_URL}`);
    for (let c of response.data.cupcakes) {
        let new_c = $(genCupcakeLi(c));
        $("#list").append(new_c);
    };
};

$("#new-form").on("submit", async function(evnt){
    evnt.preventDefault();
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const response = await axios.post(`${API_URL}`, {
        flavor,
        rating,
        size,
        image
    })

    let new_c = $(genCupcakeLi(response.data.cupcake));
    $("#list").append(new_c);
});

$("#list").on("click", "#delete-button", async function (evnt) {
    evnt.preventDefault();
    let $cupcake = $(evnt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-c-id");
    console.log(cupcakeId);
    await axios.delete(`${API_URL}/${cupcakeId}`);
    $cupcake.remove();
});

$(initCupcakes);