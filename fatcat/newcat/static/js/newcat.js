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

function popup(mylink, windowname) {
    if (! window.focus)return true;
    var href;
    if (typeof(mylink) == 'string')
        href=mylink;
    else
        href=mylink.href;
    window.open(href, windowname, 'width=400,height=200,scrollbars=yes');
    return false;
}
