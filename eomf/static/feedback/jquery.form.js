 $(document).ready(function() { 
            // bind 'myForm' and provide a simple callback function 
            $('#url_change').val(window.location.href);
            // $('#ajax_test').submit(function(e){
            //         e.preventDefault();
            //     });
            $('#ajax_test').ajaxForm(function() { 
                // $('#ajax_test').submit(function(e){
                //     e.preventDefault();
                // });
                console.log("am i there:"+x);
                $('#feedback_popup').addClass('thanks');
                $('#feedback_popup').delay(1000).fadeOut(500, feedback.closeit({
            'button':$('#feedback_button'),
            'drop':$('#feedback_drop'),
            'popup':$('#feedback_popup')
        }));
                $('#feedback_popup').delay(1000).fadeOut(500);
                //alert("Thank you for your comment!"); 
                //return 'onsuccess':True;
            }); 
        }); 