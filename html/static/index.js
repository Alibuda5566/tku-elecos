if (!data)
  alert('Fail to load data!!!')

'use strict';

var GRADES = ['全年級','大一','大二','大三','大四','大五','大六'];
var COURSES;

var selected_courses = [];
var arrange_result = [];

/* =============== Vue Directive ===============*/
Vue.config.debug = true;
Vue.config.delimiters = ['${', '}'];
var vue_inst = new Vue({
  el: '#vue-root',
  data: {
    groups : data,
    selected : selected_courses,
    GRADES: GRADES
  },
  methods: {
    is_selected: function(e){
      for (var i=0;i<selected_courses.length;i++)
        if (selected_courses[i].subject == e.subject)
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
        selected_courses.push(e);
    },
    remove_course: function(course) {
      var index = selected_courses.indexOf(course);
      selected_courses.splice(index, 1);
    },
    clear_selected: function() {
      var len = selected_courses;
      for (var i=0; i<len; i++)
        selected_courses.pop();
    },
    handle_drop: function(itemOne, itemTwo) {
      var dummy = selected_courses[itemOne.id];
      selected_courses.$set(itemOne.id, selected_courses[itemTwo.id]);
      selected_courses.$set(itemTwo.id, dummy);
    },
  }
});

function get_all_course() {
  if (COURSES) return COURSES;
  COURSES = [];
  $.each(data,function(_,group){
    $.each(group[2],function(_,dept){
      $.each(dept[2],function(_,course){
        COURSES.push(course);
      });
    });
  });
  return COURSES;
}
function find_by_subject(subject)
{
  var r = [];
  $.each(get_all_course(),function(_,e) {
    if (e.subject == subject)
      r.push(e);
  });
  return r;
}
function get_selected_subjects() {
  var r = [];
  $.each(selected_courses,function(_,e) {
    r.push(e.subject);
  });
  return r;
}
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
