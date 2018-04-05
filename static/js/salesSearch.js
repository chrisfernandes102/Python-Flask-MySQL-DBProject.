$(function(){
	$('#btnSignUp3').click(function(){
		$.ajax({
			url: '/showSalesSearch',
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