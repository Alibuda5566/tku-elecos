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
      var index = selected_courses.indexOf(course);
      vue_inst.$data.selected.splice(index, 1);
    },
    clear_selected: function() {
      var len = selected_courses.length;
      for (var i=0; i<len; i++)
        vue_inst.$data.selected.pop();
    },
    handle_drop: function(itemOne, itemTwo) {
      var dummy = selected_courses[itemOne.id];
      selected_courses.$set(itemOne.id, selected_courses[itemTwo.id]);
      selected_courses.$set(itemTwo.id, dummy);
    },
    arrange_selected: function() {
      var g = arrange();
      if (g.length == 0)
        console.log('No result');
      else
        $.each(g,function(i,e){
          if (i > 10) return ;
          console.log(i);
          var credit = 0;
          $.each(e,function(_,c){
            console.log(c.no,c.name,stringify(total_classtime(c),'index',','));
            credit += c.credit;
          });
          console.log('合計:' + e.length +'門，' + credit + '學分');
          console.log('=====================');
          if (i == 10) console.log('Results more than 10, hidden');
        })
    }
  }
});

function stringify(obj_list,key,spliter) {
  var str = '';
  spliter = spliter || '';
  $.each(obj_list,function(i,e) {
    if (i != 0)
      str += spliter;
    str += e[key];
  });
  return str;
}
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
function split_list(list) {
  var groups = [];
  $.each(list,function(_,e){
    groups.push([e]);
  });
  return groups;
}
function arrange_recurse(a,b)
{
  var groups = [];
  $.each(a,function(_,ae){
    $.each(b,function(_,be){
      if (!group_conflict(ae,be).result)
        groups.push(merge_array(ae,be));
    })
  });
  return groups;
}
function arrange()
{
  var subjects = get_selected_subjects();
  var groups = split_list(find_by_subject(subjects[0]));
  for (var i = 1; i < subjects.length; i++)
  {
    groups = arrange_recurse(groups,split_list(find_by_subject(subjects[i])));
    if (groups.length > 100)
      groups = groups.splice(0,100);
  }
  return groups;
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
