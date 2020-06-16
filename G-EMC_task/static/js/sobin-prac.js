
var model_name = "";
var current_model_id = 0;

$(function printName (){
    var testList = window.location.href;
    var subList = testList.split("?");

    var startIdx=0;
    var paramsNum="model_name";

    for(var i=0; i<subList[1].length; i++) {

      if(paramsNum[i] == subList[1][i]) {
          continue;
      }
      else {
         startIdx=i;
         break
      }
    }
    var model_id = "";

    for (var i = startIdx; i<subList[1].length; i++) {
       model_id += subList[1][i];
    }
    current_model_id = model_id;
    console.log(model_id);
    $("#makeProcess").empty();
    $("#showContents").empty();

    // 모델 명 가져오는 ajax
   $.ajax({
     url: '/pracModel',
     method: 'POST',
     data:{mID:model_id},

     success: function(response){
       var results = response;
       var first_Array = results.split(':'); // model_name 얻기 위해서
       model_name = first_Array[0];
       second_Array = first_Array[1].split('!'); // 예측시간 출력


       var predict_date = second_Array[1].split(' ');//= 예측시간 (정수형)


       var pt = $("#predict_time");
       var pt_s = '<span id="predict_time_value" style="display:inline; font-size:20px; color:#ef5b0a; font-weight:bold">&nbsp;&nbsp;&nbsp;'+ predict_date[0] +' </span>';

       pt.append(pt_s);

       var result_list = $("#printName");
       var s = "<span>"+"<span class='model_light'>Model,</span>"+model_name+"</span>";

       result_list.append(s);

       allprac(); // EMC-RF-REPORT-CY 순으로 보여지는 화면

     }, error: function(request,status,error){
       alert("에러에러 ajax");
       alert(status);
     }
   });


})

var gl_nowTime="";

function printTime() {

            var clock = document.getElementById("clock");            // 출력할 장소 선택
            var now = new Date();                                                  // 현재시간
            var nowTime ="   " + now.getFullYear() + "년 " + (now.getMonth()+1) + "월 " + now.getDate() + "일 " + now.getHours() + " :  " + now.getMinutes() + " :  " + now.getSeconds();
            gl_nowTime = now.getFullYear()+ '/' + (now.getMonth()+1) + "/" + now.getDate() +" "+ now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
            clock.innerHTML = nowTime;           // 현재시간을 출력
            setTimeout("printTime()",1000);         // setTimeout(“실행할함수”,시간) 시간은1초의 경우 1000

}


window.onload = function() {                         // 페이지가 로딩되면 실행
            printTime();
          //  printMode();
}

function stateSave(model_id){

  var size = $("input:checkbox[name=checkboxQuestion2]").length;
  var dataArray = new Array();
  //var name = document.getElementById("excel_name").value;

  $("input:checkbox[name=checkboxQuestion2]").each(function() {
    if ($(this).is(":checked") == true){
      var checked_id = this.id;
      dataArray.push(checked_id);
    }
  });
  console.log(dataArray);

  $.ajax({
    url:'/stateSave',
    method:'POST',
    data:{wish_id:model_id,
          state:dataArray.toString()},
    success: function(response){
      alert('성공');


    },error: function(e){
      alert(e);
    }
  })
}

function stateprac(model_id){
  var div = $("#state_intro");
  $("#state_intro").empty(); // 전체 페이지


  $.ajax({
    url:'/stateprac',
    method:'POST',
    data:{wish_id:model_id},
    success: function(response){
      console.log(response);

      var links = $('.thumbnail');
      links.click(function() {
           links.css({'background-color': '#6d8196','color':'white'});
           $(this).css({'background-color': 'white', 'color':'gray'});
      });


      var data = JSON.parse(response);
      var created = data.Created;
      var predicted = data.Predicted;
      var state = data.State;


      var whoJoin = $("#whoJoin"+model_id).text();
      var whoJoin_list = whoJoin.split(',');

      var intro = '<div id="intro" style=""><p> 프로젝트 시작일은  <span>'+ created + '</span>입니다.</p>';
      intro += '<p> 현재 예상되는 종료일은 <span>'+predicted + '</span>이며 , <span>' + whoJoin_list.length +'</span>명이 진행하고 있습니다.</p><br>';


      //for (var i in st)
      var color = []
      var s = "";


      $("#state_intro").append(intro);
      $("#state_intro").append("<table id='checkbox-Mode2' style='margin-left:auto; margin-right:auto;'><tr><td class='mName' style='text-align:center;width:100px;font-weight:bold'></td><td class='cName' style='text-align:center; width:150px;font-weight:bold'></td></tr></table><span id='div2'></span>");


      var state_list = ['EMC','RF','REPORT','보고 완료'];

      var i=0;


      for (var i in state){
        s="";

        var table =document.getElementById('checkbox-Mode2');
        var row = table.insertRow(-1);

        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);

        if (state[i]==1){
          // checked 완료 : color
          try{
            if (i==0) s += "<div class='checkbox-cp'><input id='emc' type='checkbox' name='checkboxQuestion2' checked>"+"<label for='emc'><span style='margin-right:30px; display:inline-block'></span><div class='chk_img' id='chk_img_emc' style='display:inline-block'></div></label></input></div>";
            else if (i==1) s += "<div class='checkbox-cp'><input id='rf' type='checkbox' name='checkboxQuestion2' checked>"+"<label for='rf'><span style='margin-right:30px; display:inline-block'></span><div class='chk_img' id='chk_img_rf' style='display:inline-block'></div></label></input></div>";
            else if (i==2) s += "<div class='checkbox-cp'><input id='rpt' type='checkbox'  name='checkboxQuestion2' checked>"+"<label for='rpt'><span style='margin-right:30px; display:inline-block'></span><div class='chk_img' id='chk_img_rpt' style='display:inline-block'></div></label></input></div>";
            else s += "<div class='checkbox-cp'><input id='cy' type='checkbox' name='checkboxQuestion2' checked>"+"<label for='cy'><span style='margin-right:30px; display:inline-block'></span><div class='chk_img' id='chk_img_cy' style='display:inline-block'></div></label></input></div>";
          }
          finally{
            cell1.innerHTML = state_list[i];
            cell2.innerHTML = s;


          }
        }

        else{
          try{
            if (i==0) s +=  "<div class='checkbox-cp'><input id='emc' type='checkbox' name='checkboxQuestion2' >"+"<label for='emc'><span style='margin-right:30px; display:inline-block'></span><div class='chk_img' id='chk_img_emc' style='display:inline-block'></div></label></input></div>";
            else if (i==1) s += "<div class='checkbox-cp'><input id='rf' type='checkbox' name='checkboxQuestion2' >"+"<label for='rf'><span style='margin-right:30px; display:inline-block'></span><div class='chk_img' id='chk_img_rf' style='display:inline-block'></div></label></input></div>";
            else if (i==2) s += "<div class='checkbox-cp'><input id='rpt' type='checkbox' name='checkboxQuestion2' >"+"<label for='rpt'><span style='margin-right:30px; display:inline-block'></span><div class='chk_img' id='chk_img_rpt' style='display:inline-block'></div></label></input></div>";
            else s += "<div class='checkbox-cp'><input id='cy' type='checkbox' name='checkboxQuestion2' >"+"<label for='cy'><span style='margin-right:30px; display:inline-block'></span><div class='chk_img' id='chk_img_cy' style='display:inline-block'></div></label></input></div>";
          }
          finally{
            cell1.innerHTML = state_list[i]; // EMC.RF 등 중 하나
            cell2.innerHTML = s;
          }
        }

      }
      $("#checkbox-Mode2").append("<button onclick='javascript:stateSave("+model_id+")' style='position:auto; margin-left:50px;'> 저 장 </button>");

    }, error: function(error){
      alert("에러:all prac");
    }
  })

}

function CreateThumb2(id,title,desc,filepath,like,hasLiked,mode_progress){

  //var boundary = $('<div>').attr({'class':'boundary'});
  // , 'style':'border:1px solid gold'
  var thumbNail = $('<div>').attr({'class':'thumbnail','style':'text-align:center; float:left; margin:15px; padding:20px; background-color:#6d8196; color:white; box-shadow: 13px 10px 20px grey; border-radius:2em ', 'id':'thumb'+id});
  //var img = $('<img>').attr({'src':filepath,'data-holder-rendered':true,'type':'button','style':'height: 150px; width: 150px; display: block'});
  var img = $('<button>').attr({'type':'button','class':'btn btnEvent' ,'id':'img_btn'+id, 'style':'padding:15px'});
  var model_name = 'img_btn'+id;


  var d_img_href = 'javascript:stateprac('+id+')';
  var img_href = $('<a>').attr({'href':d_img_href});
  var img_src = $('<img>').attr({'src':filepath,'data-holder-rendered':true,'style':'height: 100px; width: 100px; align:"center"; margint-top:10px ', 'alt':'btnImages', 'class':'btnImages' ,'onclick':''});

  var caption = $('<div>').attr('class','caption');
  var title = $('<h3>').text(title);
  var desc = $('<p style="font-size:15px">').text(desc);

  var g_btn = $('<progress>').attr({'id':'go_'+id,'value':mode_progress,'max':'100','class':'btn btn-danger active btn-block', 'style':'background-color:#dfe7ee'});

  var p = $('<p>');
  //var btn = $('<button>').attr({'id':'btn_'+id,'type':'button','class':'btn btn-secondary btn-sm'});
  var span = $('<span>').attr({'class':'glyphicon glyphicon-thumbs-up','aria-hidden':'true'});

  var likeSpan = $('<span>').attr({'aria-hidden':'true','id':'span_'+id,'style':'font-size:15px','float':'left'});
  //var with_join_show = with_join;


  if(hasLiked != ""){
    console.log(hasLiked);
    var hasLiked_list = "";
    for (var a in hasLiked){
      console.log(a);
      hasLiked_list += hasLiked[a];
      if (a<hasLiked.length-1){
        hasLiked_list += ',  ';
      }
    }
    likeSpan.html('&nbsp;with&nbsp;&nbsp;<p<p id="whoJoin'+id+'" style="font-weight:bold; display:inline; overflow:auto">'+ hasLiked_list+'</p>'); //(Number(like)-1)


  }
  else{
    likeSpan.html('&nbsp;with&nbsp;&nbsp;<p id="whoJoin'+id+'" style="font-weight:bold; display:inline">'+ "No one" + '</p>'); // with_join_show : 프로젝트 만든사람
  }

  img.append(img_href.append(img_src));

  p.append(span);
  p.append(likeSpan);


  caption.append(title);
  caption.append(desc);

  caption.append(g_btn);

  caption.append(p);

  thumbNail.append(img);
  thumbNail.append(caption);
  //mainDiv.append(thumbNail);

  //boundary.append(thumbNail);
  //return boundary;
  return thumbNail;

}

function allprac(){ // 전체 진행상황 탭
  $("#makeProcess").empty();
  $("#showContents").empty();
  // 진짜 쿠팡 처럼 이미지를 만들거다.

  $("#showContents").append("<div id='state_intro' style='width:50%; float:left; text-align:center'></div>");
  $("#showContents").append("<div id='all_wish' style='width:50%; float:left; border-left:3px solid grey; display:inline'></div>");

  var div = $('#all_wish');
  var div = $('#showContents');
  var mainDiv = $('<div>').attr({'class':'sobin'});
  div.append(mainDiv);
  $.ajax({
    url:'/getAllWishes',
    method:'GET',
    success: function(response){
    var data = JSON.parse(response);

    for (var i=0; i<data.length; i++){
      div.append(CreateThumb2(data[i].Id,data[i].Title,data[i].Description,data[i].FilePath,data[i].Like,data[i].HasLiked,data[i].rate));
    }
  }, error: function(error){
    alert("에러:all prac");
  }

})
}

function taskprac(){
  $('#showContents').empty();
  $('#makeProcess').empty();

  var ex = '<div class="col-xl-3 col-md-6 mb-4"> <div class="card border-left-primary shadow h-100 py-2"> <div class="card-body">';
  ex += '<div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1"><span id="model_regulation1"> ex) CISPR 11 & IEC 60601-1-2</span></div>';
  ex += '<div class="h5 mb-0 font-weight-bold text-gray-800"><span id="model_mode1">CT/Pano</span></div> </div> <div class="col-auto"><i class="fas fa-calendar fa-2x text-gray-300"></i> <!-- 삭제 버튼 --> </div></div></div></div></div>';
  ex += '<ul id = "already_made_List"></ul> <!----- 연이어서 add 버튼이 존재하도록 ?---> <div class="mode_add_btn"> <a href="javascript:plz_add()"> <div id ="mode_add_btn">';
  ex += '<img src="/static/images/add2.png" id ="add" style="margin-left:20px; width:50px; height:50px; display:inline"></div></a><div class="balloon_list"></div></div>';

  $('#showContents').append(ex);

  $.ajax({
    url: '/pracModel',
    method: 'POST',
    data:{mID:current_model_id},

    success: function(response){
      var results = response;
      var first_Array = results.split(':'); // model_name 얻기 위해서
      model_name = first_Array[0];
      second_Array = first_Array[1].split('!'); // 예측시간 출력


      var predict_date = second_Array[1].split(' ');//= 예측시간 (정수형)

      var strArray = second_Array[0].split(',&'); // 각 mode 별로 구분하기 위해서.
      for (var q=0; q<strArray.length-1; q++){
         var sub_Array1 = strArray[q].split('@');
         //alert(sub_Array1);

         var sub_Array2 = sub_Array1[0].split('-');

         var proc = sub_Array1[1].split(',');

         var r = sub_Array2[0];
         var v = sub_Array2[1];

         n += 1
         var t = '<li class="lili"><div class="col-xl-3 col-md-6 mb-4">';
         t += '<div class="card border-left-primary shadow h-100 py-2">';
         t += '<div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1"><span id="model_regulation'+n+'">';
         t += r
         t += '</span></div>';
         t += '<div class="h5 mb-0 font-weight-bold text-gray-800"><a href="javascript:makeProcess';
         t += '($(';
         t += "'#model_regulation"+n+"').text(),";
         t += '$(';
         t += "'#model_mode"+n+"').text(),";
         t += n + ",";
         t += '$(';
         t += "'#mode_process"+n+"').text() " + ")";
         t += '"><span id=';
         t += '"model_mode'+n+'">';
         t += v + '</span></a></div> <div id="mode_process'+n+'"'+' style="display:None">'+proc+'</div></div>';
         t += '<div class="col-auto"> <i id="current_del'+n+'" type="button" onclick="mode_delete('+n+')"> <img src="/static/images/delete.png" style="width:30px"> </i></div></div></div></div></div></li>';

         $('#already_made_List').append(t);

      }

    }
  })
}

function standardSave(){
  // 규격 저장하는 함수
  var size = $("input:checkbox[name=checkboxQuestion3]").length; // fcc,ce,kc 상태
  var dataArray = new Array();

  $("input:checkbox[name=checkboxQuestion3]").each(function() {
    if ($(this).is(":checked") == true){
      var checked_id = this.id;
      dataArray.push(checked_id);
    }
  });

  var size2 = $("input:checkbox[name=checkboxQuestion4]").length; // fcc
  var fccArray = new Array();

  $("input:checkbox[name=checkboxQuestion4]").each(function() {
    if ($(this).is(":checked") == true){
      var checked_id = this.id;
      fccArray.push(checked_id);
    }
  });

  var size3 = $("input:checkbox[name=checkboxQuestion5]").length; // ce
  var ceArray = new Array();

  $("input:checkbox[name=checkboxQuestion5]").each(function() {
    if ($(this).is(":checked") == true){
      var checked_id = this.id;
      ceArray.push(checked_id);
    }
  });

  var size4 = $("input:checkbox[name=checkboxQuestion6]").length; // kc
  var kcArray = new Array();

  $("input:checkbox[name=checkboxQuestion6]").each(function() {
    if ($(this).is(":checked") == true){
      var checked_id = this.id;
      kcArray.push(checked_id);
    }
  });

  $.ajax({
    url:'/standardSave',
    method:'POST',
    data:{wish_id:current_model_id,
          standard:dataArray.toString(),
          fcc:fccArray.toString(),
          ce:ceArray.toString(),
          kc:kcArray.toString()},
    success: function(response){
      alert('standardSave 성공');
    },error : function (e){
      alert('에러');
    }
  })
}


function taskprac_rf(){
  $('#showContents').empty();
  $('#makeProcess').empty();

  $("#showContents").append("<div style='text-align:center; font-weight:bold; font-size:20px; margin-top:40px'>시험하는 규격을 눌러주세요 <p style='font-weight:light; font-size:15px'>누르면, <span><u style='color:black;font-weight:bold;'>검은색</u></span>으로 변합니다.</p><p style='font-weight:light; font-size:15px'>각 규격별로 시험을 완료한 항목을 누르면, <span><u style='color:orange;font-weight:bold;'>주황색</u></span>으로 변합니다.</p><button onclick='javascript:standardSave()' style='text-align:center;margin-bottom:20px'>저장</button></div><br>");

  $("#showContents").append("<div id='fcc' style='width:33%; float:left; border-right:3px solid grey;border-left:3px solid grey; text-align:center;'></div>");
  $("#showContents").append("<div id='ce' style='width:33%; float:left; border-right:3px solid grey; text-align:center;'></div>");
  $("#showContents").append("<div id='kc' style='width:33%; float:left; border-right:3px solid grey;text-align:center;'></div>");

  //$("#fcc").append("<div class='checkbox-rf'><input id='fcc_logo' type='checkbox' name='checkboxQuestion3'>"+"<label for='fcc_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_fcc' style='display:inline-block'></div></label></input></div><div id='fcc_tbl'></div>");
  //$("#ce").append("<div class='checkbox-rf'><input id='ce_logo' type='checkbox' name='checkboxQuestion3'>"+"<label for='ce_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_ce' style='display:inline-block'></div></label></input></div><div id='ce_tbl'></div>");
  //$("#kc").append("<div class='checkbox-rf'><input id='kc_logo' type='checkbox' name='checkboxQuestion3'>"+"<label for='kc_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_kc' style='display:inline-block'></div></label></input></div><div id='kc_tbl'></div>");

  $.ajax({
    url:'/taskprac_rf',
    method:'POST',
    data:{mID:current_model_id},
    success: function(response){
      var stdd = JSON.parse(response);


      var standard = stdd.std_part;

      var fcc_state = [0,0,0];
      var ce_state = [0,0,0,0];
      var kc_state = [0,0,0,0];


      console.log('stdd');
      console.log(standard[0]);
      console.log(stdd.ce);
      for (var q=0; q<3; q++){
        if (standard[q]==1){
          if (q==0 & stdd.fcc.length != 0){
            fcc_state = stdd.fcc;
            fcc_state = fcc_state.split(',');
          }

          else if (q==1 & stdd.ce.length != 0){
            ce_state = stdd.ce;
            ce_state = ce_state.split(',');
          }
          else if (q==2 & stdd.kc.length != 0) {
            kc_state = stdd.kc;
            kc_state = kc_state.split(',');
        }
      }
    }

      for (var w in standard){
        if (w==0){
          // fcc
          if (standard[w]==0){
            $("#fcc").append("<div class='checkbox-rf'><input id='fcc_logo' type='checkbox' name='checkboxQuestion3'>"+"<label for='fcc_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_fcc' style='display:inline-block'></div></label></input></div><div id='fcc_tbl'></div>");

          }
          else{
            //checked
            $("#fcc").append("<div class='checkbox-rf'><input id='fcc_logo' type='checkbox' name='checkboxQuestion3' checked>"+"<label for='fcc_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_fcc' style='display:inline-block'></div></label></input></div><div id='fcc_tbl'></div>");

          }
        }

        else if (w==1){
          //ce
          if (standard[w]==0){
            $("#ce").append("<div class='checkbox-rf'><input id='ce_logo' type='checkbox' name='checkboxQuestion3'>"+"<label for='ce_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_ce' style='display:inline-block'></div></label></input></div><div id='ce_tbl'></div>");

          }
          else{
            //checked
            $("#ce").append("<div class='checkbox-rf'><input id='ce_logo' type='checkbox' name='checkboxQuestion3' checked>"+"<label for='ce_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_ce' style='display:inline-block'></div></label></input></div><div id='ce_tbl'></div>");

          }
        }

        else if (w==2){
          //kc
          if (standard[w]==0){
            $("#kc").append("<div class='checkbox-rf'><input id='kc_logo' type='checkbox' name='checkboxQuestion3'>"+"<label for='kc_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_kc' style='display:inline-block'></div></label></input></div><div id='kc_tbl'></div>");

          }
          else{
            //checked
            $("#kc").append("<div class='checkbox-rf'><input id='kc_logo' type='checkbox' name='checkboxQuestion3' checked>"+"<label for='kc_logo'><span style=' display:inline-block'></span><div class='chk_img' id='chk_img_kc' style='display:inline-block'></div></label></input></div><div id='kc_tbl'></div>");

          }
        }
      }

      // 각 div 마다 표 입력
      $("#fcc_tbl").append("<br><br><table id='checkbox-fcc' style='margin-left:auto; margin-right:auto;'><tr><td class='mName' style='text-align:center;width:100px;font-weight:bold'></td></tr><tr><td class='mName' style='text-align:center;width:100px;font-weight:bold;visibility:hidden'>야야야</td></tr></table><span id='div3'></span>");
      $("#ce_tbl").append("<br><br><table id='checkbox-ce' style='margin-left:auto; margin-right:auto;'><tr><td class='mName' style='text-align:center;width:100px;font-weight:bold'></tr></table><span id='div3'></span>");
      $("#kc_tbl").append("<br><br><table id='checkbox-kc' style='margin-left:auto; margin-right:auto;'><tr><td class='mName' style='text-align:center;width:100px;font-weight:bold'></tr></table><span id='div3'></span>");




      for (var i in fcc_state){
        var s1 = "";
        var table = document.getElementById('checkbox-fcc');
        var row = table.insertRow(-1);

        var cell1 = row.insertCell(0);
        console.log('fcc');
        console.log(fcc_state);
        if (fcc_state[i]==1 & standard[0]==1) {
          // checked
          try{
            if (i==0) s1 += "<div class='checkbox-fcc'><input id='power' type='checkbox' name='checkboxQuestion4' checked>"+"<label for='power'><span id='text_power'>Power 측정</label></input></div>";
            else if (i==1) s1 += "<div class='checkbox-fcc'><input id='con' type='checkbox' name='checkboxQuestion4' checked>"+"<label for='con'><span id='text_con'>Conducted Test</span></label></input></div>";
            else s1+= "<div class='checkbox-fcc'><input id='rad' type='checkbox' name='checkboxQuestion4' checked>"+"<label for='rad'><span id='text_rad'>Radiated Test</span></label></input></div>";
          }
          finally{
            cell1.innerHTML = s1;

          }
        }

        else{

          try{
            if (i==0) s1 += "<div class='checkbox-fcc'><input id='power' type='checkbox' name='checkboxQuestion4'>"+"<label for='power'><span id='text_power'>Power 측정</span></label></input></div>";
            else if (i==1) s1 += "<div class='checkbox-fcc'><input id='con' type='checkbox' name='checkboxQuestion4'>"+"<label for='con'><span id='text_con'>Conducted Test</span></label></input></div>";
            else s1+= "<div class='checkbox-fcc'><input id='rad' type='checkbox' name='checkboxQuestion4'>"+"<label for='rad'><span id='text_rad'>Radiated Test</span></label></input></div>";
          }
          finally{
            cell1.innerHTML = s1;

          }
        }
      }

      // CE
      for (var i in ce_state){
        var s1 = "";
        var table = document.getElementById('checkbox-ce');
        var row = table.insertRow(-1);

        var cell1 = row.insertCell(0);
    //standard[0] ==1
        if (fcc_state[i]==1 & standard[1]==1) {
          // checked
          try{
            if (i==0) s1 += "<div class='checkbox-ce'><input id='power_ce' type='checkbox' name='checkboxQuestion5' checked>"+"<label for='power_ce'><span id='text_power_ce'>Power 측정</span></label></input></div>";
            else if (i==1) s1 += "<div class='checkbox-ce'><input id='con_tx' type='checkbox' name='checkboxQuestion5' checked>"+"<label for='con_tx'><span id='text_con_tx'>Conducted Test [Tx]</span></label></input></div>";
            else if (i==2) s1 += "<div class='checkbox-ce'><input id='con_rx' type='checkbox' name='checkboxQuestion5' checked>"+"<label for='con_rx'><span id='text_con_rx'>Conducted Test [Rx]</span></label></input></div>";
            else s1+= "<div class='checkbox-ce'><input id='rad_ce' type='checkbox' name='checkboxQuestion5' checked>"+"<label for='rad_ce'><span id='text_rad_ce'>Radiated Test</span></label></input></div>";
          }
          finally{
            cell1.innerHTML = s1;

          }
        }

        else{

          try{
            if (i==0) s1 += "<div class='checkbox-ce'><input id='power_ce' type='checkbox' name='checkboxQuestion5'>"+"<label for='power_ce'><span id='text_power_ce'>Power 측정</span></label></input></div>";
            else if (i==1) s1 += "<div class='checkbox-ce'><input id='con_tx' type='checkbox' name='checkboxQuestion5'>"+"<label for='con_tx'><span id='text_con_tx'>Conducted Test [Tx]</span></label></input></div>";
            else if (i==2) s1 += "<div class='checkbox-ce'><input id='con_rx' type='checkbox' name='checkboxQuestion5'>"+"<label for='con_rx'><span id='text_con_rx'>Conducted Test [Rx]</span></label></input></div>";
            else s1+= "<div class='checkbox-ce'><input id='rad_ce' type='checkbox' name='checkboxQuestion5'>"+"<label for='rad_ce'><span id='text_rad_ce'>Radiated Test</span></label></input></div>";
          }
          finally{
            cell1.innerHTML = s1;

          }
        }
      }

      // KC

      for (var i in kc_state){
        var s1 = "";
        var table = document.getElementById('checkbox-kc');
        var row = table.insertRow(-1);

        var cell1 = row.insertCell(0);
        if (fcc_state[i]==1 & standard[2]==1) {
          // checked
          try{
            if (i==0) s1 += "<div class='checkbox-kc'><input id='power_kc' type='checkbox' name='checkboxQuestion6' checked>"+"<label for='power_kc'><span id='text_power_kc'>Power 측정</span></label></input></div>";
            else if (i==1) s1 += "<div class='checkbox-kc'><input id='con_nor' type='checkbox' name='checkboxQuestion6' checked>"+"<label for='con_nor'><span id='text_con_nor'>Conducted Test [Normal]</span></label></input></div>";
            else if (i==2) s1 += "<div class='checkbox-kc'><input id='con_3' type='checkbox' name='checkboxQuestion6' checked>"+"<label for='con_3'><span id='text_con_3'>Conducted Test [Low,High,Hummid]</span></label></input></div>";
            else s1+= "<div class='checkbox-kc'><input id='rad_kc' type='checkbox' name='checkboxQuestion6' checked>"+"<label for='rad_kc'><span id='text_rad_kc'>Radiated Test</span></label></input></div>";
          }
          finally{
            cell1.innerHTML = s1;

          }
        }

        else{

          try{
            if (i==0) s1 += "<div class='checkbox-kc'><input id='power_kc' type='checkbox' name='checkboxQuestion6'>"+"<label for='power_kc'><span id='text_power_kc'>Power 측정</span></label></input></div>";
            else if (i==1) s1 += "<div class='checkbox-kc'><input id='con_nor' type='checkbox' name='checkboxQuestion6'>"+"<label for='con_nor'><span id='text_con_nor'>Conducted Test [Noraml]</span></label></input></div>";
            else if (i==2) s1 += "<div class='checkbox-kc'><input id='con_3' type='checkbox' name='checkboxQuestion6'>"+"<label for='con_3'><span id='text_con_3'>Conducted Test [Low,High,Hummid]</span></label></input></div>";
            else s1+= "<div class='checkbox-kc'><input id='rad_kc' type='checkbox' name='checkboxQuestion6'>"+"<label for='rad_kc'><span id='text_rad_kc'>Radiated Test</span></label></input></div>";
          }
          finally{
            cell1.innerHTML = s1;

          }
        }

} // kc 끝
},error: function(e){
      alert('에러다');
    } // 에러 끝
  }) //
} // 함수 끝

var current_model_name="";

function goprac(){
  $('#showContents').empty();
  $('#makeProcess').empty();
  // 현재 저장되어있는 각 모드별 진행상황 엑셀시트를 제작한다 : download 버튼도 (엑셀파일)
  // 다시 새로운 내용으로 db에서 불러온다.
  $.ajax({

    url: '/pracModel',
    method: 'POST',
    data:{mID:current_model_id},

    success: function(response){
      var results = response;
      console.log(results);
      var first_Array = results.split(':'); // model_name 얻기 위해서
      model_name = first_Array[0];
      current_model_name = model_name;

      $('#showContents').empty();
      var a = "<ul id=already_made_List>"
      $("#showContents").append(a);

      var strArray = first_Array[1].split(',&'); // 각 mode 별로 구분하기 위해서.
      //var tempArray = strArray.split('$');
      //strArray = tempArray[0];
      //rate = tempArray[1];
      //console.log(strArray);
      //console.log("")
      console.log("goprac");
      console.log(current_model_id);
      console.log(strArray);

      for (var q=0; q<strArray.length-1; q++){
         var sub_Array1 = strArray[q].split('@');

         var sub_Array2 = sub_Array1[0].split('-');

         var proc = sub_Array1[1].split(',');

         var r = sub_Array2[0];
         var v = sub_Array2[1];
         var rate ='?'

         n += 1
         var t = '<li class="lili"><div class="col-xl-3 col-md-6 mb-4">';
         t += '<div class="card border-left-primary shadow h-100 py-2">';
         t += '<div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1"><span id="model_regulation'+n+'">';
         t += r
         t += '</span></div>';
         t += '<div class="h5 mb-0 font-weight-bold text-gray-800">';
         t += '<span id=';
         t += '"model_mode'+n+'">';
         t += v + '</span></a></div> <div id="mode_process'+n+'"'+' style="display:None">'+proc+'</div></div>';
         t += '<div class="col-auto"> <a href="javascript:coupang('+ current_model_id + ','+ '$(';
         t +=  "'#model_regulation";
         t += n +"'"+ ').text(),$(';
         t += "'#model_mode";
         t += n+"'" + ').text()'+','+n+')"><i> 진행률 <i id="Rate" style="font-weight:bold"></i><i>%</i></i> </a></div></div></div></div></div></li></ul>';
         // 삭제버튼은 빼고

         $('#already_made_List').append(t);


      }
    }, error: function(request,status,error){
      alert("에러에러 ajax");
      alert(status);
    }
  });
}

function goprac_rf(){
  $('#showContents').empty();
  $('#makeProcess').empty();
  // 현재 저장되어있는 각 모드별 진행상황 엑셀시트를 제작한다 : download 버튼도 (엑셀파일)
  // 다시 새로운 내용으로 db에서 불러온다.


      // standard (FCC,CE,KC 체크 여부 불러오기)
      $.ajax({
        url:'/goprac_rf',
        method:'POST',
        data:{mID:current_model_id},
        success: function(response){
          // 일단은 FCC CE KC 중 현재 계획한 모드는 ?
          var res = JSON.parse(response);


      // 해당 규격들 object 나타나면서 각 세부항목 얼마나 진행됬는지 보여줘 (프로그레스 바로)

      standard_name = ['FCC', 'CE', 'KC'];

      var standard = res.standard;
      console.log('standard');

      standard = standard.split(',');
      console.log(standard);
      //standard = [1,0,1]

      $("#showContents").append("<ul id='already_made_List'>");

      for(var a in standard){
        console.log('a')
        console.log(a)
        if (standard[a]==1){

          var t = '<li class="standardLi"><div class="col-xl-3 col-md-6 mb-4">';
          t += '<div class="card border-left-primary shadow h-100 py-2" style="width:500px">';
          t += '<div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">';
          t += '<span style="font-family:'+ " 'Balsamiq Sans'"+', cursive; font-size:30px; font-weight:bold">'+standard_name[a];
          t += '</span></div>';
          t += '<div class="h5 mb-0 font-weight-bold text-gray-800"></div></div></div>';

          t += "<table id='standard-Mode"+a+"' style='float:left'><tr><td class='mName' style='text-align:center;width:500px'> 분류 </td><td class='cName' style='text-align:center; width:500px'> 현재 진행률 </td> <td style='text-align:center;'></td></tr></table>";

          $("#already_made_List").append(t);


          if (a==0){
            var md = 'standard-Mode'+a;

            for (var i=0; i<3; i++){

              var table =document.getElementById(md);
              var row = table.insertRow(-1);

              var cell1 = row.insertCell(0);
              var cell2 = row.insertCell(1);
              var cell3 = row.insertCell(2);

              var sub1="";

              if (i==0){
                sub1 = "<div style='text-align:center'>" + 'Power 측정' + "</div>";
              }

              if (i==1){
                sub1 = "<div style='text-align:center'>" + 'Conducted Test' + "</div>";
              }

              if (i==2){
                sub1 = "<div style='text-align:center'>" + 'Radiated Test' + "</div>";
              }


              var sub2="";
              var pgName = 'progressTag' + i;

              sub2 = '<progress class="'+pgName+'" value="0" max="100"/></div>';

              if (i==2){
                sub2 = '<progress class="'+pgName+'" value="0" max="100"/></div></li></ul>';
              }

              cell1.innerHTML = sub1;
              cell2.innerHTML = sub2;
              cell3.innerHTML = '50%';

              var rate = 0.5;
              tag(rate,pgName)


            }
          } // FCC

          else if (a==1){
            console.log("ce");
            var md = 'standard-Mode'+a;

            for (var i=0; i<4; i++){
              var table =document.getElementById(md);
              var row = table.insertRow(-1);

              var cell1 = row.insertCell(0);
              var cell2 = row.insertCell(1);
              var cell3 = row.insertCell(2);

              var sub1="";

              if (i==0){
                sub1 = "<div style='text-align:center'>" + 'Power 측정' + "</div>";
              }

              if (i==1){
                sub1 = "<div style='text-align:center'>" + 'Conducted Test [Tx]' + "</div>";
              }

              if (i==2){
                sub1 = "<div style='text-align:center'>" + 'Conducted Test [Rx]' + "</div>";
              }

              if (i==3){
                sub1 = "<div style='text-align:center'>" + 'Radiated Test' + "</div>";
              }


              var sub2="";
              var pgName = 'progressTag' + i+10;

              sub2 = '<progress class="'+pgName+'" value="0" max="100"/></div>';

              if (i==2){
                sub2 = '<progress class="'+pgName+'" value="0" max="100"/></div></li></ul>';
              }

              cell1.innerHTML = sub1;
              cell2.innerHTML = sub2;
              cell3.innerHTML = '60%';

              var rate = 0.6;
              tag(rate,pgName)


            }

          }//CE

          else if (a==2){
            var md = 'standard-Mode'+a;
            for (var i=0; i<4; i++){
              var table =document.getElementById(md);
              var row = table.insertRow(-1);

              var cell1 = row.insertCell(0);
              var cell2 = row.insertCell(1);
              var cell3 = row.insertCell(2);

              var sub1="";

              if (i==0){
                sub1 = "<div style='text-align:center'>" + 'Power 측정' + "</div>";
              }

              if (i==1){
                sub1 = "<div style='text-align:center'>" + 'Conducted Test [normal]' + "</div>";
              }

              if (i==2){
                sub1 = "<div style='text-align:center'>" + 'Conducted Test[Low/High/Hum]' + "</div>";
              }

              if (i==3){
                sub1 = "<div style='text-align:center'>" + 'Radiated Test' + "</div>";
              }


              var sub2="";
              var pgName = 'progressTag' + i+20;

              sub2 = '<progress class="'+pgName+'" value="0" max="100"/></div>';

              if (i==2){
                sub2 = '<progress class="'+pgName+'" value="0" max="100"/></div></li></ul>';
              }

              cell1.innerHTML = sub1;
              cell2.innerHTML = sub2;
              cell3.innerHTML = '30%';

              var rate = 0.3;
              tag(rate,pgName)


            }


          } // KC


        } // 등록된거일 때만ㅇ


      } //for 문 끝
    }
  })
    }// 함수끝


    // for progress tag in HTML
function tag (rate,pgName) {
  var pgName_dot = '.'+pgName;
  let progress = document.querySelector(pgName_dot)
  let interval = 1
  let updatesPerSecond = 1000 / 60 // 올라가는 속도
  let end = progress.max * rate // 몇 퍼센트인가

  function animator () {
    progress.value = progress.value + interval
    if ( progress.value + interval < end){
      setTimeout(animator, updatesPerSecond);
    } else {
      progress.value = end
    }
  }

  setTimeout(() => {
    animator()
  }, updatesPerSecond)
}


function coupang(mid,r,v,number){
  // 여기서 진행률 확인하고 값 업데이트 해주자.
  $('#makeProcess').empty();

  $.ajax({
    url: '/coupang',
    method: 'POST',
    data:{mID:mid,
          r:r,
          v:v},

    success: function(response){
      var results = response;
      console.log("---------------");
      console.log(results);
      var firstArray = results.split('@');
      var strArray = firstArray[0].split(',');

      var comArray = firstArray[1].split(',');

      console.log(strArray); // 전체 모드
      console.log(strArray.length);
      console.log(comArray); // 완료된 모드들


      var a = strArray.length;
      var b = comArray.length;
      var rate = b/a*100;
      console.log('rate');

      rate = rate.toFixed(2);
      console.log(rate);
      $('#Rate').append('<i>'+rate+'</i>');

      //alert(strArray);
      //alert(strArray.length);
      $('#makeProcess').empty();
      var reg = r;
      var ver = v;

      var intro = "<br>";
      intro += "<span style='margin-left:30px'><input type='text' id='excel_name'";
      intro += "placeholder"+ '="' + current_model_name+ ".xlsx 파일을 확인하세요."+ '"'+ "disabled";
      intro += " style='display:inline; text-align:center'></span>";
      intro += '<a href="JavaScript:coupang_detail(';
      intro += mid + ','+'$(' + "'#model_regulation" +number+"').text(),";
      intro += '$(' + "'#model_mode" +number+"').text()";
      intro += ')"> <img src="/static/images/dw2-removebg-preview.png" style="width:50px; height:50px; margin-left:20px">';
      intro += "</a><p></p><p style='margin-left:40px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;시험 완료한 해당 시험모드 버튼을 클릭하세요 </p><br><table id='checkbox-Mode' style='float:left'><tr><td class='mName' style='text-align:center;width:230px'>선택한 모드명</td><td class='cName' style='text-align:center; width:150px'>완료 여부</td></tr></table>";
      intro += "<div class='predict' style='float:right'></div>";
      $('#makeProcess').append(intro);

      // ios 이모티콘 만들어진 다음, 이미 checked 되있는 completed mode는 빨간색으로 변해있도록.
      var index = new Array();

      for (var j in comArray){
        for (var k in strArray){
          console.log(comArray[j],strArray[k]);
          if (comArray[j]==strArray[k]){
            index.push(k);
          }
        }
      }
      var sub_k=0;
      console.log("==============");
      console.log(index);


      for (var i in strArray){
          var table =document.getElementById('checkbox-Mode');
          var row = table.insertRow(-1);

          var cell1 = row.insertCell(0);
          var cell2 = row.insertCell(1);

          if (index[sub_k]==i){
            var sub1="";
            sub1 += "<div style='text-align:center'>" + strArray[i] + "</div>";

            var sub2="";

            sub2 += "<div class='checkbox-ios' style='float:left'> <input class='checkbox-ios__toggle' id='checkboxQuestion-"+strArray[i]+"' name='checkboxQuestion' type='checkbox' checked>";
            sub2 += "<label class='checkbox-ios__label' for='checkboxQuestion-"+strArray[i]+"'><span class='checkbox-ios__value left'>";
            sub2 += 'Not yet' +'</span>';
            sub2 += "<span class='checkbox-ios__value right'>";
            sub2 += 'Complete' + '</span>';
            sub2 += "</label></input></div><br>";

            cell1.innerHTML = sub1;
            cell2.innerHTML = sub2;

            sub_k += 1;

          }
          else{
            var sub1="";
            sub1 += "<div style='text-align:center'>" + strArray[i] + "</div>";

            var sub2 ="";

            sub2 += "<div class='checkbox-ios' style='float:left'> <input class='checkbox-ios__toggle' id='checkboxQuestion-"+strArray[i]+"' name='checkboxQuestion' type='checkbox'>";
            sub2 += "<label class='checkbox-ios__label' for='checkboxQuestion-"+strArray[i]+"'><span class='checkbox-ios__value left'>";
            sub2 += 'Not yet' +'</span>';
            sub2 += "<span class='checkbox-ios__value right'>";
            sub2 += 'Complete' + '</span>';
            sub2 += "</label></input></div><br>";

            cell1.innerHTML = sub1;
            cell2.innerHTML = sub2;
          }
        }
      }, error: function(error){
      alert('에러다다다다');
    }


  //var main_area = $('#showContents');
  //var s = "<a href=''>" + "<img src=/static/images/again.png width=50px height=50px> </a>"
  //s += "<a href=''>" + "<img src=/static/images/dw2.png width=50px height=50px> </a>"
  //main_area.append(s);
});
}


function coupang_detail(mid,r,v){
  var size = $("input:checkbox[name=checkboxQuestion]").length;
  var dataArray = new Array();
  //var name = document.getElementById("excel_name").value;

  $("input:checkbox[name=checkboxQuestion]").each(function() {
    if ($(this).is(":checked") == true){
      var checked_id = this.id;
      checked_id = checked_id.split('-');
      dataArray.push(checked_id[1]);
    }
  });


  $.ajax({
    url:"/coupang_detail",
    method:'POST',
    data:{
      mID: mid,
      r:r,
      v:v,
      file_name:name,
      checked:dataArray.toString()}, // 왜 배열 자체는 넘길수 없을까..?
    success: function(response){
      if (response ==""){
        alert('F A I L');
        return
      }

      var pd_str = "";
      pd_str += "<span id='pd_time'>예상되는 테스트 소요시간은 " + parseInt(response) +"시간 입니다.</span>"
      $(".predict").append(pd_str);
      // response >> machine learning
    },error: function(error){
      alert(error);
    }
  });
}

var n = 1

function plz_add(name){
    var already_made_list = $("#already_made_List");
    $(".balloon_list").empty();
    $("#mode_add_btn").empty();
    var add_btn = $("#mode_add_btn");
    var z ="";
    z += "<form action='#'><a href='javascript:mode_add_btn_DB()'>"+"<img src='/static/images/send.png' style='width:50px;height:50px;margin-left:20px'>";
    add_btn.append(z);

    var balloon_list = $(".balloon_list");
    // 입력 양식 말풍선
    var s="";
    s = "<div class='balloon_03'>";
    s += "<input class='add_input' type='text' id='regulation' placeholder='규격명' onfocus='this.value=";
    s += '""; return true;';
    s += "'";
    s += " ><input  class='add_input' type='text' id='mode-name'placeholder='모드명' onfocus='this.value=";
    s += '""; return true;';
    s += "'";
    s += "/></div></a>";
    balloon_list.append(s);

}

function makeProcess(r,v,num,proc){

  $("#makeProcess").empty(); // 중복클릭했을 때, append 되는게 아니라 새로 불러들이는 방식으로.
  var sampleProcess = $("#makeProcess");
  var model_regulation = r;
  var model_mode = v;
  var before_proc="";
  before_proc = proc;
  if (proc===undefined){
    before_proc = "You Can Select the process of this Mode! ";
  }

  var s = '<table id="testTable">';
  s += '<colgroup> <col style="width: 1%">';
  s += '<col style="width: 70%"> <col style="width: 20%"> </colgroup>';
  s += '<p style="color:#242096; font-weight:bold;';
  s += 'font-family:"Font Awesome 5 Brands"; font-size:15px;';
  s += '">"'+model_regulation+'"</p>';

  s += '<p style="color:#242096; font-weight:bold;';
  s += 'font-family:"Font Awesome 5 Brands"; font-size:15px;';
  s += '">"'+model_mode+'"</p>';

  s += '<p style="color:#242096; font-weight:bold;';
  s += 'font-family:"Font Awesome 5 Brands"; font-size:15px;';
  s += '">"'+before_proc+'"</p>';

  s += '<div class="makeProcess"> <button type="button" id="send" onclick="send('+ num +')"> SEND </button> <i>&nbsp;해당 모드에 관한 process를 모두 선택한 후, "SEND" 버튼을 누릅니다.</i><br><div class="fake" id="result"></div> </div>';

  s += '<thead> <tr> <th> # </th> <th>Contents</th> <th>Delete</th> </tr> </thead>';
  s += '<tbody> <tr> <td><input type="checkbox" id="checkbox" disabled="disabled"></td> <td id="contents">---- [Example] Surge ----</td> <td> <button type="button" class="btn_delete" >Delete</button> </td> </tr>';

  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">RE</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">CE</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">Harmonic</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">Flicker</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">RS</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">CS</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">ESD</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">MF</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">EFT/Burst</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">Surge</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '<tr> <td><input type="checkbox" id="checkbox" checked="checked" disabled="disabled"></td> <td id="contents">V-Dip/Interuption</td> <td> <button type="button" class="btn_delete" onclick="deleteClick()">Delete</button> </td> </tr>';
  s += '</tbody> </table> <input id="text_add" type="text" name="newAdd" placeholder="새로운 process 추가" autocomplete=off onfocus="this.value=';
  s += '"";return true;';
  s += '"/>';
  s += '<input type="button" id="btn_add" value=" 추가 " onclick="action_add()" /></div>';

  sampleProcess.append(s);

}

function mode_delete(num){
    alert('R U sure to remove this mode?');
    var idx = '#current_del'+num;
    var parent = $(idx).closest('li');

    var r = $("#model_regulation"+num).text();
    var v = $("#model_mode"+num).text();

    $.ajax({
      url:"/removeMode",
      method:"POST",
      data:{model_id:current_model_id,
            model_regulation:r,
            model_mode:v
      },
      success: function(response){
        alert("삭제 성공");
      },error:function(error){
        alert("에러다 이마마마");
      }

    });
    parent.remove();
  }

function mode_add_btn_DB(){
    var r = $('#regulation').val();
    var v = $('#mode-name').val();


    if (r==""){
      alert("규격 내용을 입력하세용");
      return;
    }
    if (v==""){
      alert("모드명을 입력하세용");
      return;
    }
    // 여기서 이전에 입력한 mode인지 체크해서 거르기
    var check_result="";
    $.ajax({
      url:'/checkMode',
      method:'POST',
      async:false,
      data:{model_id:current_model_id,
            regulation:r,
            mode:v},
      success: function(response){
        check_result=response;
        if (response=='True'){
          alert("이미 존재하는 모드입니다. 확인해주세요");
          return;
        } //존재한다.
      },error: function(error){
        alert("에러ㅔ");
      }
    });
    if (check_result=='True'){
      return;
    }
    n += 1;

    var t = '<li class="lili"><div class="col-xl-3 col-md-6 mb-4">';
    t += '<div class="card border-left-primary shadow h-100 py-2">';
    t += '<div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1"><span id="model_regulation'+n+'">';
    t += r
    t += '</span></div>';
    t += '<div class="h5 mb-0 font-weight-bold text-gray-800"><a href="javascript:makeProcess';
    t += '($(';
    t += "'#model_regulation"+n+"').text(),";
    t += '$(';
    t += "'#model_mode"+n+"').text(),"+n+")";
    t += '"><span id=';
    t += '"model_mode'+n+'">';
    t += v + '</span></a></div></div>';
    t += '<div class="col-auto"> <i id="current_del'+n+'" type="button" onclick="mode_delete('+n+')"> <img src="/static/images/delete.png" style="width:30px"> </i></div></div></div></div></div></li>';

    $('#already_made_List').append(t);
    return n; // 해당 n return해서 send 버튼할 때 활용
}

function action_add(){
  var text_add = $("#text_add").val();
  if (text_add==""){
    alert("내용을 입력하세용");
    return
  }
  var s = "<tr><td><input type='checkbox' id='checkbox' checked='checked' disabled='disabled'></td><td id='contents'>"+text_add+"</td>";
  s += "<td><button type='button' class='btn_delete' onclick='deleteClick()'>Delete</button></td></tr>";
  $("#testTable tr:last").after(s);

};

function deleteClick(){
  var eventTarget = document.getElementsByClassName('btn_delete');
  console.log(eventTarget);
  for ( var i = 0; i<eventTarget.length; i++){
    eventTarget[i].addEventListener('click',function(){
      console.log('event동작');
    });
  };
  for (var i=1; i<eventTarget.length; i++) {
    // for문을 1부터 돌림으로써 가장 위에있는 example surge는 삭제 안되도록 함.
    eventTarget[i].addEventListener('click', function() {
    var parent = document.querySelector('#testTable tbody')
    parent.removeChild(this.parentElement.parentElement)
    i --
  });
};

};

function checkDB(){
  var model_regulation = $("#regulation").text();
  var model_mode = $("#model_mode").text();
  var db_key = {'model_regulation':model_regulation,
                'model_mode':model_mode};

  var returnObject="";
  $.ajax({
    url:"/Account/processSearch",
    dataType:"text",   // ajax 통신을 통해 주고 받는 데이터형을 설정해야 한다. 멋모르고 json 하면 ㄴㄴ
    contentType:"application/json; charset=UTF-8",
    type:"post",
    data:JSON.stringify(db_key), // ajax_object를 JSON string형태로 변환
    async:false,
    success: function(response){
      alert('DB에 존재하는지 안하는지 체크 완료');
      // 만약 db에 존재한다면 저장되어있는 mode_process 목록 가져와서 보여주기.
      //response - DB에 존재하는 값을 불러오는 작업
      showDB(response);
  }, error : function(request,status,error){
    alert(db_key);
    alert("AJAX_ERROR __ 개발자를 부르세요");
  }

});
};

function showDB(result){
    $("#result").empty();
    var show_list = $("#result");
    var result = result;
    result=result.replace('[',"");
    var result_and_date=result.split(']');
    var result_item_list = result_and_date[0].split(',');
    var result_date = result_and_date[1];
    result_date = result_date.replace(']',"");

    var s = "<br><span> Updated : "+result_date+"</span>";
    show_list.append(s);
    for(var item in result_item_list){

      var s = "<div class='multi-line-highlightor'> <span> <span id='result_item'>";
      s += result_item_list[item] + "</span></span></div>";

      show_list.append(s);
  }
};

function send(num){
    $("#result").empty();  // send 버튼 눌렀을 때 새로운 값들이 들어가도록 하기 위해
    var result_list = $("#result");
    var rowData = new Array();
    var tdArr = new Array();
    var chk = $("input[id=checkbox]:checked");
    console.log(chk);


    //체크된 체크박스 값을 가져온다.
    chk.each(function(i){  // each함수는 반복문과 같은 역할을 한다.
        var tr = chk.parent().parent().eq(i);
        var td = tr.children();

        //체크된 row의 모든 값을 배열에 담는다.
        rowData.push(tr.text());
        var result = td.eq(1).text();

        // 가져온 ㄱ밧을 배열에 담는다.
        tdArr.push(result);
        console.log("결과:",result);


        var s = "<div class='multi-line-highlightor'> <span> <span id='result_item'>";
        s +=result+"</span></span></div>";

        result_list.append(s);
        //tdArr을 보내고자 하는 대상과 함께 보내면 된다 (추가 구현)
    });

    var rID = "#model_regulation"+num;
    var vID = "#model_mode"+num;

    var r = $(rID).text();
    var v = $(vID).text();

    console.log(model_name);
    var btn_save = "<br><form method='POST' enctype='multipart/form-data' id='ajaxTestForm' name='ajaxTestForm'>";
    btn_save += "<input type='hidden' name='model_regulation' style='display:none'/>"+r+"<br>";
    btn_save += "<input type='hidden' name='model_mode' style='display:none'/>"+v+"<br>";
    btn_save += "<input type='hidden' name='mode_process' style='display:none'/>"+tdArr+"</form>";

    //result_list.append(btn_save); 굳이 안보여줘도 되니까
    console.log(tdArr);

    var tdArr_str=""
    for (var a in tdArr){
      tdArr_str += tdArr[a];
      tdArr_str += ',';
    }
    console.log(tdArr_str);
    $.ajax({
      url:"/modeProcessSave", // 여기에 어디 저장소랑 통신할지를 표시해야한다.
      method:"POST",
      data:{model_id:current_model_id,
            model_regulation:r,
            model_mode:v,
            mode_process:tdArr_str,
            created:gl_nowTime}, // ajax_object를 JSON string형태로 변환
      success: function(response){
        //alert('DB에 저장 성공');

        //console.log(ajax_object);
      },
      error : function(request,status,error){
        alert("AJAX_ERROR __ 개발자를 부르세요");
      }
    });

    //$("#result").html(tdArr);
  };


  function upClick(obj){
    var idStr = "#" + obj;

    var prevHtml = $(idStr).prev().html();

    if (prevHtml == null || $(idStr).prev().attr("id") == 'mark0'){
      alert('최상위 리스트입니다!');
      return;
    }

    var preobj = $(idStr).prev().attr("id");
    var currobj = $(idStr).attr("id");
    var currHtml = $(idStr).html();

    $(idStr).html(prevHtml); // 값 변경
    $(idStr).prev().html(currHtml);
    $(idStr).prev().attr("id","TEMP_TR"); // id 값도 변경
    $(idStr).attr("id",preobj);
    $("#TEMP_TR").attr("id",currobj);
  }

  function downClick(obj){
    var idStr = "#" + obj;
    var nextHtml = $(idStr).next().html();
    var nextobj = $(idStr).next().attr("id");


    if (nextHtml == null || nextobj == 'mark0'){
      alert('최하위 리스트입니다!');
      return;
    }
    var nextobj = $(idStr).next().attr("id");
    var currobj = $(idStr).attr("id");
    var currHtml = $(idStr).html();
    $(idStr).next().html(currHtml);

    $(idStr).html(nextHtml); // 값 변경
    $(idStr).next().attr("id","TEMP_TR"); // id 값도 변경
    $(idStr).attr("id",nextobj);
    $("#TEMP_TR").attr("id",currobj);
  }




  function deleteClick2(){
    var eventTarget = document.getElementsByClassName('btn_delete2');
    console.log(eventTarget);
    for ( var i = 0; i<eventTarget.length; i++){
      eventTarget[i].addEventListener('click',function(){
        console.log('event동작');
      });
    };
    for (var i=1; i<eventTarget.length; i++) {
      // for문을 1부터 돌림으로써 가장 위에있는 example surge는 삭제 안되도록 함.
      eventTarget[i].addEventListener('click', function() {
      var parent = document.querySelector('#testTable2 tbody')
      parent.removeChild(this.parentElement.parentElement)
      i --
    });
  };

  };

  // 파일 등록 '성적서 작성완료' 버튼
  var fileList = new Array();
  var totalFileSize = 0;

  function uploadFile() {
      // 등록할 파일 리스트
      var uploadFileList = Object.keys(fileList);

      console.log(uploadFileList);
      console.log(fileList);

      // 파일이 있는지 체크
      if (uploadFileList.length == 0) {
          // 파일등록 경고창
          alert("파일이 없습니다.");
          return;
      }

      // 용량을 500MB를 넘을 경우 업로드 불가
      if (totalFileSize > 500) {
          // 파일 사이즈 초과 경고창
          alert("총 용량 초과\n총 업로드 가능 용량 : " + maxUploadSize + " MB");
          return;
      }

      if (confirm("성적서를 작성 하시겠습니까?")) {
          // 등록할 파일 리스트를 formData로 데이터 입력
          //var form = $('#uploadForm');
          //var size = uploadFileList.length;
          //var excelList = new Array();
          //for (var a=0; a<size; a++){
          //  excelList.push(fileList[a].name);
          //}


          var conArray = new Array();
          var fileArray = new Array();

          var chk = $("input[id=checkbox2]:checked");

          console.log('chk');
          console.log(chk);

          // 체크된 체크박스 값을 가져온다.
          chk.each(function(i){ // each문은 반복문과 같은 역할을 한다.
            var tr = chk.parent().parent().eq(i);
            var td = tr.children();


            var contents = td.eq(1).text();
            var dataFile = td.eq(2).text();

            conArray.push(contents);
            fileArray.push(dataFile);
          })



          $.ajax({
              url : "/uploadFile",
              data : {
                      conList : JSON.stringify(conArray),
                      fileList : JSON.stringify(fileArray)},
              method : 'POST',

              success : function(result) {
                  if (result.data.length > 0) {
                      alert("성공");
                      location.reload();
                  } else {
                      alert("실패");
                      location.reload();
                  }
              }
              , beforeSend: function(){
                $('.wrap-loading').removeClass('display-none');
              }

              ,complete: function(){
                $('.wrap-loading').addClass('display-none');
              }

              ,error:function(){
                $('.wrap-loading').addClass('display-none');
                alert('에러발생');
              }
          });



      }
  }

  // TDS RF
  function report_rf(){

    $("#showContents").empty();
    $("#makeProcess").empty();



    var s ="";
    s += '<table id="testTable2" style="margin-left:auto; margin-right:auto">';
    //; return false;
    s += '<div class="makeProcess"><input type="button" onclick="javascript:uploadFile()" id="btn_final_upload" class="btn bg_01" value="성적서 작성완료" style="margin-left:44%"><br><br>';
    s += '<p style="font-size:15px; margin-left:30%">성적서의 <3.3 전기적 조건> 항목에 입력하고자 하는 데이터를 순서대로 나열한 후 버튼을 누릅니다.</p></div>';


    s += '<thead><th> # </th> <th>Contents</th> <th> Data File </th> </th><th>Delete</th> <th>▲</th> <th>▼</th></thead>';
    s += '<tbody><tr id="mark0"><td><input type="checkbox" id="checkbox2" disabled="disabled"></td> <td id="contents"> --(예) 2.4G WLAN(802.11b)--</td> <td> PPR21_TDS_2.4G WLAN_KC(RF)_802._11b.xls</td><td> <button type="button" class="btn_delete2" onclick="deleteClick2()" >Delete</button> </td><td><button type="button" class="btn_up" >▲</button></td><td><button type="button" class="btn_down" >▼</button></td>';

    s += '</tr></tbody> </table><br> <input  id="text_add2" type="text"  style="display:inline-block; margin-left:35%; margin-bottom:20px" name="newAdd" placeholder="작성하고 싶은 시험모드명 작성" autocomplete=off onfocus="this.value=';
    s += "'';return true;";
    s += '"/>';
    //s += '<input type="button" id="btn_add" style="margin-left:auto; margin-right:auto" value=" 추가 " onclick="action_add()" /></div>';

    var f = "";

    f += '<form name="uploadForm" id="uploadForm" enctype="multipart/form-data" method="post">';
    f += '<div id="dropZone" style="width: 80%; height: 20%; border-style: dashed; border-color: gray; margin:10px; margin-left:10%">';
    f += '<div id="fileDragDesc" style="font-size:30px; font-weight:bold; color:#2f2d2d; margin-bottom:-20px"><img src = "/static/images/drag2.png" style= "width:180px; height:150px;"> Drag & Drop files here</div>';
    f += '<div class="upload-btn-wrapper" style="display:inline"><input type="file" id="input_file" multiple="multiple"/><button class="upload-btn" style="margin-left:45%;margin-bottom:20px">파일선택</button></div>';
    f += '<table id="fileListTable" width="100%" border="0px">';
    f += '<tbody id="fileTableTbody"></tbody></table></div></form>';
    f += '</div>';


    $("#showContents").empty();
    $("#makeProcess").empty();

    $("#showContents").append("<div class='report_rf'></div>");
    $("#showContents").append('<div class="wrap-loading display-none"><div><img src="/static/images/loading.gif"/></div></div>');


    $(".report_rf").append(s); // 기본 테이블 틀
    $(".report_rf").append(f);

    $(document).ready(function() {

                $("#input_file").bind('change', function() {
                    selectFile(this.files);
                    //this.files[0].size gets the size of your file.
                    //alert(this.files[0].size);
        });
      });


            // 파일 리스트 번호
            var fileIndex = 0;
            // 등록할 전체 파일 사이즈
            //var totalFileSize = 0;
            // 파일 리스트
            //var fileList = new Array();
            // 파일 사이즈 리스트
            var fileSizeList = new Array();
            // 등록 가능한 파일 사이즈 MB
            var uploadSize = 50;
            // 등록 가능한 총 파일 사이즈 MB
            var maxUploadSize = 500;

            $(function() {
                // 파일 드롭 다운
                fileDropDown();
            });

            // 파일 드롭 다운
            function fileDropDown() {
                var dropZone = $("#dropZone");
                //Drag기능
                dropZone.on('dragenter', function(e) {
                    e.stopPropagation();
                    e.preventDefault();
                    // 드롭다운 영역 css
                    dropZone.css('background-color', '#E3F2FC');
                });
                dropZone.on('dragleave', function(e) {
                    e.stopPropagation();
                    e.preventDefault();
                    // 드롭다운 영역 css
                    dropZone.css('background-color', '#FFFFFF');
                });
                dropZone.on('dragover', function(e) {
                    e.stopPropagation();
                    e.preventDefault();
                    // 드롭다운 영역 css
                    dropZone.css('background-color', '#E3F2FC');
                });
                dropZone.on('drop', function(e) {
                    e.preventDefault();
                    // 드롭다운 영역 css
                    dropZone.css('background-color', '#FFFFFF');

                    var files = e.originalEvent.dataTransfer.files;
                    if (files != null) {
                        if (files.length < 1) {
                            /* alert("폴더 업로드 불가"); */
                            console.log("폴더 업로드 불가");
                            return;
                        } else {
                            selectFile(files)
                        }
                    } else {
                        alert("ERROR");
                    }
                });
            }

            // 파일 선택시
            function selectFile(fileObject) {
                var files = null;

                if (fileObject != null) {
                    // 파일 Drag 이용하여 등록시
                    files = fileObject;
                } else {
                    // 직접 파일 등록시
                    files = $('#multipaartFileList_' + fileIndex)[0].files;
                }

                // 다중파일 등록
                if (files != null) {

                    if (files != null && files.length > 0) {
                        $("#fileDragDesc").hide();
                        $("fileListTable").show();
                    } else {
                        $("#fileDragDesc").show();
                        $("fileListTable").hide();
                    }

                    for (var i = 0; i < files.length; i++) {
                        // 파일 이름
                        var fileName = files[i].name;
                        var fileNameArr = fileName.split("\.");
                        // 확장자
                        var ext = fileNameArr[fileNameArr.length - 1];

                        var fileSize = files[i].size; // 파일 사이즈(단위 :byte)
                        console.log("fileSize="+fileSize);
                        if (fileSize <= 0) {
                            console.log("0kb file return");
                            return;
                        }

                        var fileSizeKb = fileSize / 1024; // 파일 사이즈(단위 :kb)
                        var fileSizeMb = fileSizeKb / 1024;    // 파일 사이즈(단위 :Mb)

                        var fileSizeStr = "";
                        if ((1024*1024) <= fileSize) {    // 파일 용량이 1메가 이상인 경우
                            console.log("fileSizeMb="+fileSizeMb.toFixed(2));
                            fileSizeStr = fileSizeMb.toFixed(2) + " Mb";
                        } else if ((1024) <= fileSize) {
                            console.log("fileSizeKb="+parseInt(fileSizeKb));
                            fileSizeStr = parseInt(fileSizeKb) + " kb";
                        } else {
                            console.log("fileSize="+parseInt(fileSize));
                            fileSizeStr = parseInt(fileSize) + " byte";
                        }

                        /* if ($.inArray(ext, [ 'exe', 'bat', 'sh', 'java', 'jsp', 'html', 'js', 'css', 'xml' ]) >= 0) {
                            // 확장자 체크
                            alert("등록 불가 확장자");
                            break; */
                        if ($.inArray(ext, [ 'hwp', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'png', 'pdf', 'jpg', 'jpeg', 'gif', 'zip' ]) <= 0) {
                            // 확장자 체크
                            /* alert("등록이 불가능한 파일 입니다.");
                            break; */
                            alert("등록이 불가능한 파일 입니다.("+fileName+")");
                        } else if (fileSizeMb > uploadSize) {
                            // 파일 사이즈 체크
                            alert("용량 초과\n업로드 가능 용량 : " + uploadSize + " MB");
                            break;
                        } else {
                            // 전체 파일 사이즈
                            totalFileSize += fileSizeMb;

                            // 파일 배열에 넣기
                            fileList[fileIndex] = files[i];

                            // 파일 사이즈 배열에 넣기
                            fileSizeList[fileIndex] = fileSizeMb;

                            // 업로드 파일 목록 생성
                            addFileList(fileIndex, fileName, fileSizeStr);

                            // 파일 번호 증가
                            fileIndex++;
                        }
                    }
                } else {
                    alert("ERROR");
                }
            }


            // 업로드 파일 목록 생성
            var tr_id_num = 0
            function addFileList(fIndex, fileName, fileSizeStr) {
                /* if (fileSize.match("^0")) {
                    alert("start 0");
                } */

                var html = "";
                html += "<tr id='fileTr_" + fIndex + "'>";
                html += "    <td id='dropZone' class='left' >";
                html += '* '+fileName + " (" + fileSizeStr +") ";
                        //+ "<a href='#' onclick='deleteFile(" + fIndex + "); return false;' class='btn small bg_02'> 삭제</a>"

                //        + "<input value='삭제' type='button' href='#' onclick='deleteFile(" + fIndex + "); return false;'>"
                html += "    </td>"

                html += "</tr>"


                var text_add2 = document.getElementById("text_add2").value

                tr_id_num ++;
                var tr_id = 'mark'+tr_id_num;
                tr_id = String(tr_id);



                var s = "<tr id="+tr_id+"><td><input type='checkbox' id='checkbox2' checked='checked' disabled='disabled'></td><td id='contents'>"+text_add2+"</td>";
                s += "<td>"+fileName+"</td><td><button type='button' class='btn_delete2' onclick='deleteClick2()'>Delete</button></td>";
                s += "<td><button type='button' class='btn_up' onclick='upClick("+'"'+tr_id+'"'+")'>▲</button></td> <td><button type='button' class='btn_down' onclick='downClick("+'"'+tr_id+'"'+")'>▼</button></td></tr>";

                if (text_add2 == ''){
                  alert('시험모드명을 입력하세요!');
                  return
                }
                console.log("+++++++++++++++++++");
                console.log(s);
                $("#testTable2 tr:last").after(s);
                $('#fileTableTbody').append(html);


            }

            // 업로드 파일 삭제
            function deleteFile(fIndex) {
                console.log("deleteFile.fIndex=" + fIndex);
                // 전체 파일 사이즈 수정
                totalFileSize -= fileSizeList[fIndex];

                // 파일 배열에서 삭제
                delete fileList[fIndex];

                // 파일 사이즈 배열 삭제
                delete fileSizeList[fIndex];

                // 업로드 파일 테이블 목록에서 삭제
                $("#fileTr_" + fIndex).remove();

                console.log("totalFileSize="+totalFileSize);

                if (totalFileSize > 0) {
                    $("#fileDragDesc").hide();
                    $("fileListTable").show();
                } else {
                    $("#fileDragDesc").show();
                    $("fileListTable").hide();
                }
            }



          }
