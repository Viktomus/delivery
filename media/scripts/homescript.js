
function SelectQuantity(itemName)
{
    var selectionDoc = document.getElementById('SelectionDiv' + itemName);

    if (selectionDoc.style.display == "none")
        selectionDoc.style.display = "";
    else
        selectionDoc.style.display = "none";
}

function ConfirmQuantity(itemName)
{
    var quantityInput = document.getElementById("Input" + itemName);
    quantity = quantityInput.value;

    if (quantity == "")
        quantity = 1

    window.location.href = "http://localhost:8000/checkout/" + itemName + "/" + quantity;
}
