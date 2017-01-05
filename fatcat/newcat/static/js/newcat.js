function searchFunction(queryInput, queryField) {
  var input, filter, table, tr, td, i;
  input = document.getElementById(queryInput);
  filter = input.value.toUpperCase();
  table = document.getElementById("testCaseTable");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    query_field = tr[i].getElementsByTagName("td")[queryField];
    if (query_field) {
      if (query_field.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function saveSettings(){
sessionStorage.setItem("formdata",formToString($("#createTestCaseForm")));
}

function loadSettings(){
    var storedform = sessionStorage.getItem("formdata");
    stringToForm(storedform,$("#createTestCaseForm"));
    }

function formToString(filledForm) {
  formObject = new Object();
    filledForm.find("input, select, textarea").each(function() {
        if (this.id) {
            elem = $(this);
            if (elem.attr("type") == 'checkbox' || elem.attr("type") == 'radio') {
                formObject[this.id] = elem.attr("checked");
            } else {
                formObject[this.id] = elem.val();
            }
        }
    });
    formString = JSON.stringify(formObject);
    return formString;
}

function stringToForm(formString, unfilledForm) {
    formObject = JSON.parse(formString);
    unfilledForm.find("input, select, textarea").each(function() {
        if (this.id) {
            id = this.id;
            elem = $(this);
            if (elem.attr("type") == "checkbox" || elem.attr("type") == "radio" ) {
                elem.attr("checked", formObject[id]);
            } else {
                elem.val(formObject[id]);
            }
        }
    });
}

