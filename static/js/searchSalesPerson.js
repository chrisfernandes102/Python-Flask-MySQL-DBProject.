$(function(){
	$('#btnSignUp7').click(function(){
		$.ajax({
			url: '/showSalesPerson',
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