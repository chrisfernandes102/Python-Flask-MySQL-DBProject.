$(function(){
	$('#btnSignUp4').click(function(){
		$.ajax({
			url: '/showSearch',
			data: $('form').serialize(),
			type: 'GET',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});