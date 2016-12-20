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

function pageTable(tableName){
    $(tableName).tablesorterPager({container: $("#pager")});
}