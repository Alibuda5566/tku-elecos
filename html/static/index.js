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
    selected : {
      required: [],
      optional: [],
      all: [],
      arranged: []
    },
    GRADES: GRADES
  },
  methods: {
    is_selected: function(e,type){
      type = type || vue_inst.$data.selected.all;
      for (var i=0;i<type.length;i++)
        if (type[i].subject == e.subject)
          return true;
      return false;
    },
    add_dept: function (dept_data,term,obligatory) {
      $.each(dept_data,function(i,e) {
        if (e.term == term && (obligatory === undefined || e.obligatory == obligatory))
          vue_inst.add_course(e);
      });
    },
    add_course: function(e,type) {
      type = type || vue_inst.$data.selected.required;
      if (type != vue_inst.$data.selected.all)
        vue_inst.remove_course(e);
      type.push(e);
      if (type != vue_inst.$data.selected.all)
        vue_inst.add_course(e,vue_inst.$data.selected.all);
    },
    remove_course: function(course,type) {
      if (!type)
      {
        vue_inst.remove_course(course,vue_inst.$data.selected.required);
        vue_inst.remove_course(course,vue_inst.$data.selected.optional);
        vue_inst.remove_course(course,vue_inst.$data.selected.all);
      }
      else {
        var index = type.indexOf(course);
        if (index != -1)
          type.splice(index, 1);
        if (type != vue_inst.$data.selected.all)
          vue_inst.remove_course(course,vue_inst.$data.selected.all);
      }
    },
    clear_selected: function(type) {
      if (!type) {
        vue_inst.clear_selected(vue_inst.$data.selected.all);
        vue_inst.clear_selected(vue_inst.$data.selected.required);
        vue_inst.clear_selected(vue_inst.$data.selected.optional);
      }
      else {
        var len = type.length;
        for (var i=0; i<len; i++)
          type.pop();
      }
    },
    handle_drop: function(itemOne, itemTwo) {
      // TODO: need fix
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
            console.log(c.no,c.name,stringify(c.classtime,'index',','));
            credit += c.credit;
          });
          console.log('合計:' + e.length +'門，' + credit + '學分');
          console.log('=====================');
          if (i == 10) console.log('Results more than 10, hidden');
        })
      Vue.set(vue_inst.$data,'arranged',g);
    },
    index_filter: function(group, index) {
      var r = [];
      $.each(group,function(_,l) {
        $.each(l.classtime,function(_,ct) {
          if (ct.index == index)
            r.push(l);
        })
      })
      return r;
    },
    hashcolor: hashStringToColor,
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
function get_selected_subjects(type) {
  type = type || vue_inst.$data.selected.all;
  var r = [];
  $.each(type,function(_,e) {
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
    groups = arrange_recurse(groups,split_list(find_by_subject(subjects[i])),true);
    //TODO: temporary reduce time cost
    if (groups.length > 100)
      groups = groups.splice(0,100);
  }
  return groups;
}
function conflict(a,b,simple)
{
  var result = {result: false, conflicts: []};
  $.each(a.classtime, function(ia,ea) {
    $.each(b.classtime, function(ib,eb){
      if (ea.index == eb.index)
      {
        result.result = true;
        if (!simple)
          result.conflicts.push(ea.index);
      }
    });
  });
  return result;
}
function group_conflict(a,b,simple)
{
  var result = {result: false, conflicts: []};
  $.each(a,function(ia,ea){
    $.each(b,function(ib,eb){
      var temp = conflict(ea,eb,simple);
      if (temp.result == true)
      {
        result.result = true;
        if (!simple)
          result.conflicts = merge_array(result.conflicts, temp.conflicts);
      }
    })
  })
  return result;
}

function djb2(str){
  var hash = 5381;
  for (var i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash) + str.charCodeAt(i); /* hash * 33 + c */
  }
  return hash;
}

function hashStringToColor(str) {
  var hash = djb2(str.toString());
  var r = (hash & 0xFF0000) >> 16;
  var g = (hash & 0x00FF00) >> 8;
  var b = hash & 0x0000FF;
  return "#" + ("0" + r.toString(16)).substr(-2) + ("0" + g.toString(16)).substr(-2) + ("0" + b.toString(16)).substr(-2);
}
