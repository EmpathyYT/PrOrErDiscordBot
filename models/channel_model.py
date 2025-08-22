from dataclasses import dataclass

@dataclass
class ChannelModel:
    is_testing: bool = False
    is_release: bool= False
    is_bug_report: bool = False
    is_closed: bool = False
    is_suggestion:bool = False
