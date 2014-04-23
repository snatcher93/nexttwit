$(document).ready(function() {
	$('#follow').click(function() {
		bootbox.confirm('사용자를 팔로우하시겠습니까?', 
			function(response) {
				if (!response) return;
				$('#follow_form')
					.attr({'method':'post', 'action':'{{url_for("follow_user", userid=profile_user.userid)}}'})
					.submit();
		});
	});
				
	$('#unfollow').click(function() {
		bootbox.confirm('사용자를 팔로우하지 않겠습니까?', 
			function(response) {
				if (!response) return;
				$('#follow_form')
					.attr({'method':'post', 'action':'{{url_for("unfollow_user", userid=profile_user.userid)}}'})
					.submit();
		});
	});	
});