
data_hx = [];

function tag(name, content){
    return "<"+name+">"+content+"</"+name+">";
};

function radio(name, value){
    return $(tag("input", value))
        .attr("type", "radio")
        .attr("name", name)
        .attr("value", value)
        ;
};

function create_radio_buttons(){
    names = col_names(get_current_result());
    for (var i=0; i<names.length; i++){
        $('#xfilter').append( radio('col_radio', names[i]));
    }
};

function get_checked_cols(){
    var checked_arr = [];
    $('.col_check:checked').each(function(idx, elt){
        checked_arr.push(elt.value) });
    return (checked_arr);

};

function get_current_result(){
    return ($('.output1').contents()[0].data);
};

function get_current_names(){
    return col_names(get_current_result());
};


function chop_current_result(){
    // fetch inputs
    current = get_current_result().split('\n');
    n = $('#n_chop').val();
    // alter data
    head = current.slice(0, n).join('\n');
    result = current.slice(n, current.length).join('\n');
    // display result
    display_result(result);
};



function secondary_display(){
    if (  get_current_result() === 'No Results')
        return ('None');
    var casename = $('#da_form select :selected')[0].text;
    var result_length = csv2obarray(  get_current_result()).length;
    result_length = 'total rows: ' + result_length;
/*
    var stuff = current_tickets();
    stuff.push('tickets');
*/
    var stuff = [];
    stuff.push('\n');
    stuff.push('\n');

    stuff.push(result_length);
    stuff.push(casename);
    stuff.reverse();
    return stuff.join('\n');
};




function filter_on(colname, value){
    // Given colname and value, filter the current result set (as
    // a list of objects).
    // Return the filtered sublist.
    // filter_on('docid', '42')

    var current_obs = csv2obarray(  get_current_result());
    var res = [];
    for (var i=0; i<current_obs.length; i++){
        if (current_obs[i][colname].match(value))
            res.push(current_obs[i]);
    }
    return (res);
};


function show_filtered(name, value){
    // Given colname and value, filter the current result set and
    // display.
    //     filtered = show_filtered('docid', 42);
    //     filtered = show_filtered('date', '15:41');

    var names = get_current_names();
    var filtered = filter_on(name, value);
    var body = ob_array2csv(filtered, names);
    var head = names.join(',');
    var new_csv = [head, body].join('\n')
    $('.output1').text(new_csv);
    $('.output2').text( secondary_display() );
    data_hx.push( new_csv);
};


function go_filter(){
    // Get the current parameters from the form and display a
    // filtered version of the current result set.
    var radio_col = $("input[type='radio'][name='col_radio']:checked").val();
    var filter_val = $("#filter_val").val();
    var filtered = show_filtered(radio_col, filter_val);
    };
    


function prev_result(){
    // Like the name says, replace the current result set with the previous.
    //
    data_hx.pop();
    $('.output1').text(data_hx[data_hx.length-1]);
    $('.output2').text( secondary_display() );
};
    
   
function show_control1(event){
    // Make sort controls invisible, show case selection controls,
    // and clear the output displays.
    $('#div_sort').css('display', 'none');
    $('#da_form').css('display', 'block');
    $('.output1').text('clear');
    $('.output2').text('clear');
};



function get_json_result(event){
    event.preventDefault(); // !!!!!!! prevent page reload !!!!!!! //
    thing = $.ajax({
        type: 'GET',
        url: 'SPCS20RNSA.txt',
        success: function(returned_data, textStatus, jqXHR){
            console.log('success');
            display_result(returned_data);
        },
    })
};



function display_result(s){
    $('.output1').text( s );
    $('.output2').text( secondary_display() );
    data_hx.push( s );
    $('#div_sort').css('display', 'block');
    $('#da_form').css('display', 'none');
};




function import_code(event){
    url = '../icons/data_structures.js';
    $.getScript(url, function(data, textStatus, jqxhr) {
        console.log(data); //data returned
        console.log(textStatus); //success
        console.log(jqxhr.status); //200
        console.log('Load was performed.');
        }).done(function(script, textStatus) {
              console.log( textStatus );
        }).fail(function(jqxhr, settings, exception) {
                grr = jqxhr;
                console.log( "Triggered ajaxError handler." );
                console.log(jqxhr.status); //500
                console.log(settings);
                console.log(exception);
                gjqxhr = jqxhr;
                gsettings = settings;
                gexception = exception;
    });
};


function yoohoo(event){ console.log('yoohoo'); };


$(document).ready(function(){
//    import_code(event);  // data structures //
    yoohoo(event);
    setInterval(yoohoo , 1000*60); // every 1 min.
    // !!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!
    // NOTE we could use something like yoohoo to refresh
    //      basic data q min.
    // !!!!!!!!!!!!!!!!!!!!!!!
    $('#submit').click( function(event){get_json_result(event);} );
    $('#filter_submit').click( function(event){go_filter(event);} );
    $('#prev_result').click( function(event){prev_result(event);} );
    $('#to_control1').click( function(event){show_control1(event);});
    $('#chop_submit').click( function(event){chop_current_result(event);});
    $('#radio_make').click( function(event){create_radio_buttons(event);});

});
    


