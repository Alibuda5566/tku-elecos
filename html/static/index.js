if (!data)
  alert('Fail to load data!!!')

'use strict';

/* =============== Vue Directive ===============*/
Vue.config.debug = true;
Vue.config.delimiters = ['${', '}'];
var vue_inst = new Vue({
  el: '#vue-root',
  data: {
    groups : data,
    selected : []
  },
  methods: {
    add_dept: function (dept_data,term, obligatory) {
      $.each(dept_data,function(i,e) {
        if (e.term == term && (obligatory === undefined || e.obligatory == obligatory))
        {
          var selected = false;
          for (var i=0;i<vue_inst.$data.selected.length;i++)
          {
            if (vue_inst.$data.selected[i].subject == e.subject)
            {
              selected = true;
              break;
            }
          }
          if (!selected)
            vue_inst.$data.selected.push(e);
        }
      });
    },
    remove_course: function(course) {
      var index = vue_inst.$data.selected.indexOf(course);
      vue_inst.$data.selected.splice(index, 1);
    }
  }
});
