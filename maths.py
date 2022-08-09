def getTeamRedZonePercent(team):
    if team == "ATL":
        return .638
    if team == "BAL":
        return .540
    if team == "BUF":
        return .539
    if team == "CAR":
        return .673
    if team == "CHI":
        return .556
    if team == "CIN":
        return .580
    if team == "CLE":
        return .654
    if team == "DAL":
        return .617
    if team == "DEN":
        return .500
    if team == "DET":
        return .700
    if team == "GB":
        return .623
    if team == "HOU":
        return .621
    if team == "IND":
        return .642
    if team == "JAX":
        return .623
    if team == "KC":
        return .576
    if team == "LV":
        return .771
    if team == "LAC":
        return .642
    if team == "LAR":
        return .531
    if team == "MIA":
        return .526
    if team == "MIN":
        return .559
    if team == "NE":
        return .537
    if team == "NO":
        return .435
    if team == "NYG":
        return .521
    if team == "NYJ":
        return .608
    if team == "PHI":
        return .662
    if team == "PIT":
        return .540
    if team == "SF":
        return .543
    if team == "SEA":
        return .508
    if team == "TB":
        return .523
    if team == "TEN":
        return .517
    if team == "WSH":
        return .593
    return 1
    
# RB FER = total yds + 40% x (carries x yds/carry)/(week to week st.dev of carries) + 60% x (red zone carries x team red zone td %)
def getRBRating(statistic, team):
    totalyds = statistic['rushing']['yards'] + statistic['receiving']['yards']
    carries = statistic['rushing']['attempts']
    blah = 1
    ydspercarry = statistic['rushing']['avg_yards']
    redzonecarries = statistic['rushing']['redzone_attempts']
    redzoneteampct = getTeamRedZonePercent(team)
    return totalyds + (.4 * ((carries * ydspercarry) / blah)) + (.6 * (redzonecarries * redzoneteampct)) 

# WR FER = total yds + 40% x (targets x yards/target)/(week to week  st.dev of targets) + 60% x (red zone targets x team red zone td %)
def getWRRating(statistic, team):
    totalyds =  statistic['receiving']['yards'] 
    if 'rushing' in statistic:
        totalyds += statistic['rushing']['yards']
    targets = statistic['receiving']['targets']
    blah = 1
    ydspertarget = statistic['receiving']['avg_yards']
    redzonetargets = statistic['receiving']['redzone_targets']
    redzoneteampct = getTeamRedZonePercent(team)
    return totalyds + (.4 * ((targets * ydspertarget) / blah)) + (.6 * (redzonetargets * redzoneteampct))