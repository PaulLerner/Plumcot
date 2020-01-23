#!/usr/bin/env python
# encoding: utf-8

import json
DISTANCE_THRESHOLD=0.5

def annotation_to_GeckoJSON(annotation, distances, colors={}):
    """
    Parameters:
    -----------
    annotation: `pyannote.core.Annotation`
        proper pyannote annotation for speaker identification/diarization
    colors: `dict`
        speaker id : consistent color

    Returns:
    --------
    gecko_json : a JSON `dict` based on the demo file of https://github.com/gong-io/gecko/blob/master/samples/demo.json
        should be written to a file using json.dump
    """

    gecko_json=json.loads("""{
      "schemaVersion" : "2.0",
      "monologues" : [  ]
    }""")
    for segment, track, label in annotation.itertracks(yield_label=True):
        distance=distances.get(segment)
        distance=distance.get(label) if distance else None
        distance= distance if distance !="<NA>" else None
        if distance:
            if distance > DISTANCE_THRESHOLD:
                label=f"?{label}"

        color=colors.get(label) if colors else None
        
        gecko_json["monologues"].append(
            {
                "speaker":{
                    "id":label,
                    "start" : segment.start,
                    "end" : segment.end,
                    "color": color
                },
                "terms":[
                    {
                        "start" : segment.start,
                        "end" : segment.end
                    }
                ]
        })
    return gecko_json
