function GetSuffix()
{
    $suffix = get-content "suffix.txt" -ea SilentlyContinue;

    if (!$suffix)
    {
        $suffix = -join ((65..90) + (97..122) | Get-Random -Count 5 | % {[char]$_});

        add-content "suffix.txt" $suffix;
    }

    return $suffix.tolower();
}
function SelectSubscription()
{
    #select a subscription
    $subs = Get-AzSubscription | Select-Object
    if($subs.GetType().IsArray -and $subs.length -gt 1){
            Write-Host "You have multiple Azure subscriptions - please select the one you want to use:"
            for($i = 0; $i -lt $subs.length; $i++)
            {
                    Write-Host "[$($i)]: $($subs[$i].Name) (ID = $($subs[$i].Id))"
            }
            $selectedIndex = -1
            $selectedValidIndex = 0
            while ($selectedValidIndex -ne 1)
            {
                    $enteredValue = Read-Host("Enter 0 to $($subs.Length - 1)")
                    if (-not ([string]::IsNullOrEmpty($enteredValue)))
                    {
                        if ([int]$enteredValue -in (0..$($subs.Length - 1)))
                        {
                            $selectedIndex = [int]$enteredValue
                            $selectedValidIndex = 1
                        }
                        else
                        {
                            Write-Output "Please enter a valid subscription number."
                        }
                    }
                    else
                    {
                        Write-Output "Please enter a valid subscription number."
                    }
            }
            $selectedSub = $subs[$selectedIndex].Id
            Select-AzSubscription -SubscriptionId $selectedSub
            az account set --subscription $selectedSub
    }
}