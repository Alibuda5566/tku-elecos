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
    selected : (storage.fetch() || {
      required: [],
      optional: [],
      confirmed: [],
      all: [],
      arranged: []
    }),
    GRADES: GRADES
  },
  watch:
  {
    'selected': {
      handler: function(val){
        storage.save(val);
      },
      deep: true
    },
    'select_group': function(){
      Vue.set(vue_inst.$data,'select_dept',vue_inst.$data.select_group[2][0]);
    }
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
        vue_inst.remove_course(course,vue_inst.$data.selected.confirmed);
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
        vue_inst.clear_selected(vue_inst.$data.selected.confirmed);
      }
      else {
        var len = type.length;
        for (var i=0; i<len; i++)
          type.pop();
      }
    },
    handle_drop: function(itemOne, itemTwo, type) {
      // TODO: need fix
      var dummy = type[itemOne.id];
      type.$set(itemOne.id, type[itemTwo.id]);
      type.$set(itemTwo.id, dummy);
    },
    handle_drop_confirmed: function(itemOne, itemTwo) {
      this.handle_drop(itemOne, itemTwo, vue_inst.$data.selected.confirmed);
    },
    handle_drop_required: function(itemOne, itemTwo) {
      this.handle_drop(itemOne, itemTwo, vue_inst.$data.selected.required);
    },
    handle_drop_optional: function(itemOne, itemTwo) {
      this.handle_drop(itemOne, itemTwo, vue_inst.$data.selected.optional);
    },
    arrange_selected: function() {
      var g = arrange();
      /*if (g.length == 0)
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
        })*/
      Vue.set(vue_inst.$data,'arranged',g);
      Vue.set(vue_inst.$data,'selected_arranged',vue_inst.$data.arranged[0]);
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
    count_credit: function(data) {
      var count = 0;
      var i = data.length;
      while (i--) {
        count += data[i].credit;
      }
      return count;
    },
    set_hover: function(element, hover) {
      Vue.set(element,'hover',hover);
    },
    hashcolor: hashStringToColor
  },
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
    var i = e.classtime.length;
    while(i--)
    {
      if (!vue_inst.$data.selected.arrange_night)
        if (e.classtime[i].index % 100 > 10)
          return;
      if (!vue_inst.$data.selected.arrange_week)
        if (e.classtime[i] >= 600)
          return;
    }
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
function set_subjects_state(subject, failed)
{
  var i = vue_inst.$data.selected.required.length;
  while(i--)
  {
    if (vue_inst.$data.selected.required[i].subject == subject)
    {
      vue_inst.$data.selected.required[i].fail = failed;
      return;
    }
  }
  var i = vue_inst.$data.selected.optional.length;
  while(i--)
  {
    if (vue_inst.$data.selected.optional[i].subject == subject)
    {
      Vue.set(vue_inst.$data.selected.optional[i],'fail',failed);
      return;
    }
  }
}
function arrange()
{
  var requireds = get_selected_subjects(vue_inst.$data.selected.required);
  var optionals = get_selected_subjects(vue_inst.$data.selected.optional);
  var confirmed = vue_inst.$data.selected.confirmed;
  var subjects = merge_array(requireds,optionals);
  var groups = [merge_array(confirmed,[])];
  for (var i = 1; i < subjects.length; i++)
  {
    var c = find_by_subject(subjects[i]);
    if (!c.length)
    {
      set_subjects_state(subjects[i], true);
      continue;
    }
    var t_groups = arrange_recurse(groups,split_list(c),true);
    if (t_groups.length == 0)
    {
      set_subjects_state(subjects[i], true);
      continue;
    }
    else
      set_subjects_state(subjects[i], false);

    //TODO: temporary reduce time cost
    if (t_groups.length > 100)
      t_groups = t_groups.splice(0,100);
    groups = t_groups;
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
function hashStringToColor(str) {
  // str to hash
  for (var i = 0, hash = 0; i < str.length; hash = str.charCodeAt(i++) + ((hash << 5) - hash));
  // int/hash to hex
  for (var i = 0, colour = "#"; i < 3; colour += ("00" + ((hash >> i++ * 8) & 0xFF).toString(16)).slice(-2));
  return colour;
}

$(function() {
  Vue.set(vue_inst.$data,'select_group',vue_inst.$data.groups[0]);
})
