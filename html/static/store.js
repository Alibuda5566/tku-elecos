/*jshint unused:false */
(function (exports) {
  'use strict';
  var STORAGE_KEY = 'selected_courses';
  exports.storage = {
    fetch: function () {
      var data = localStorage.getItem(STORAGE_KEY);
      if (data)
        return JSON.parse( data || '[]');
    },
    save: function (data) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }
  };
})(window);
