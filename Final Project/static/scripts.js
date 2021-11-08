$(document).ready(function(){

    // code to read selected table row cell data (values).
    $("#patients_table").on('click','.btnEdit',function(){
        // get the current row
        var currentRow=$(this).closest("tr");

        var col1 = currentRow.find("td:eq(0)").text(); // get current row ID
        var col2 = currentRow.find("td:eq(1)").text(); // get current row Patient_name
        var col3 = currentRow.find("td:eq(2)").text(); // get current row Patient_phone
        var col4 = currentRow.find("td:eq(3)").text(); // get current row Patient_mail
        var col5 = currentRow.find("td:eq(4)").text(); // get current row due_date

        sessionStorage.setItem('patient_id', col1)
        sessionStorage.setItem('patient_name', col2)
        sessionStorage.setItem('patient_phone', col3)
        sessionStorage.setItem('patient_mail', col4)
        sessionStorage.setItem('due_date', col5)

        window.location.href = "/edit_patient";
    });

    // code to read selected row ID in case of DELETE btn is clicked
    $("#patients_table").on('click','.btnDel',function(){
        // get the current row
        var currentRow=$(this).closest("tr");

        var col1 = currentRow.find("td:eq(0)").text(); // get current row ID
        var response;
         $.ajax({
            url: '/edit_patient',
            type: 'PUT',
            data: {'patient_id': col1},

         });
        window.location.href = '/all_patients';
    });
});

function edit_patient() {
    document.getElementById('pt_id').value = sessionStorage.getItem('patient_id')
    document.getElementById('pt_name').value = sessionStorage.getItem('patient_name')
    document.getElementById('pt_phone').value = sessionStorage.getItem('patient_phone')
    document.getElementById('pt_mail').value = sessionStorage.getItem('patient_mail')
    document.getElementById('d_date').value = sessionStorage.getItem('due_date')
}