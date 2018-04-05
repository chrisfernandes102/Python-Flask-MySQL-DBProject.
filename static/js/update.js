$(function(){
	$('#btnSignUp4').click(function(){
		$.ajax({
			url: '/showSalesUpdate',
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
