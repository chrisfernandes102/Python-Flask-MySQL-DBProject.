$(function(){
	$('#btnSignUp5').click(function(){
		$.ajax({
			url: '/showCarAdd',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
