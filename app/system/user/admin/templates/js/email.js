
;(function() {
  var that = $.extend(true, {}, admin_module)
  fetch(that)
  TEMPLOADFUNS[that.hash] = function() {
    fetch(that,1)
  }
})()
function fetch(that,norefresh) {
  M.ajax(
    {
      url: that.own_name + '&c=admin_set&a=doGetemailSetup'
    },
    function(result) {
      let data = result.data
      Object.keys(data).map(item => {
        $(`[name=${item}]`).val(data[item])
      })
      !norefresh && that.obj.metCommon()
    }
  )
}
