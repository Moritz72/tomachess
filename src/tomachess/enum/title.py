from enum import Enum


class Title(str, Enum):
    GM = "grand_master"
    IM = "international_master"
    FM = "fide_master"
    CM = "candidate_master"
    WGM = "woman_grand_master"
    WIM = "woman_international_master"
    WFM = "woman_fide_master"
    WCM = "woman_candidate_master"
    NONE = "none"
