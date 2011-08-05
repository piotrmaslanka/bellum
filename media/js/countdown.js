function countdown(fieldname, timeleft)
{
	if (timeleft < 0)
	{
                if (document.global_allowReload == null) document.global_allowReload = true;
                if (document.global_allowReload) location.reload();
                else document.global_requireReload = true;
		return 0;
	}

	var seconds = new String(Math.floor(timeleft%60));
	if (seconds.length == 1) seconds = "0"+seconds;
	var minutes = new String(Math.floor(timeleft / 60)%60);
	if (minutes.length == 1) minutes = "0"+minutes;

        try 
        {
            document.getElementById(fieldname).innerHTML = Math.floor(timeleft/3600)+':'+minutes+':'+seconds;
        } catch(err)
        {
            // fuck you there is no error. Error does not exist.
        }
	setTimeout("countdown('"+fieldname+"',"+(timeleft-1)+")", 1000);
}