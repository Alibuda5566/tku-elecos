if (!data)
  alert('Fail to load data!!!')

'use strict';

GRADES = ['全年級','大一','大二','大三','大四','大五','大六'];

/* =============== Vue Directive ===============*/
Vue.config.debug = true;
Vue.config.delimiters = ['${', '}'];
var vue_inst = new Vue({
  el: '#vue-root',
  data: {
    groups : data,
    selected : [],
    GRADES: GRADES
  },
  methods: {
    is_selected: function(e){
      for (var i=0;i<vue_inst.$data.selected.length;i++)
        if (vue_inst.$data.selected[i].subject == e.subject)
          return true;
      return false;
    },
    add_dept: function (dept_data,term, obligatory) {
      $.each(dept_data,function(i,e) {
        if (e.term == term && (obligatory === undefined || e.obligatory == obligatory))
          vue_inst.add_course(e);
      });
    },
    add_course: function(e) {
      if (!vue_inst.is_selected(e))
        vue_inst.$data.selected.push(e);
    },
    remove_course: function(course) {
      var index = vue_inst.$data.selected.indexOf(course);
      vue_inst.$data.selected.splice(index, 1);
    }
  }
});
function merge_array() {
  var result = []
  $.each(arguments, function(i,item){
    $.each(item,function(i,e){result.push(e)});
  });
  return result;
}
function total_classtime(c)
{
  return merge_array(c.classtime,c.lab_classtime);
}
function conflict(a,b)
{
  var result = {result: false, conflicts: []};
  $.each(total_classtime(a), function(ia,ea) {
    $.each(total_classtime(b), function(ib,eb){
      if (ea.index == eb.index)
      {
        result.result = true;
        result.conflicts.push(ea.index);
      }
    });
  });
  return result;
}
function group_conflict(a,b)
{
  var result = {result: false, conflicts: []};
  $.each(a,function(ia,ea){
    $.each(b,function(ib,eb){
      var temp = conflict(ea,eb);
      if (temp.result == true)
      {
        result.result = true;
        result.conflicts = merge_array(result.conflicts, temp.conflicts);
      }
    })
  })
  return result;
}
