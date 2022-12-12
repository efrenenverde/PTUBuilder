import { useState } from "react";
import jsonData from "./../feats-remake.json";
import classes from './Builder.module.css';

// Del JSON quité lo de Blessed+Damned y puse algún que otro Rank X bien

const Builder = () => {
  const [charLevel, setCharLevel] = useState(1);
  const [charFeatList, setCharFeatList] = useState([]);
  const [charEdgeList, setEdgeList] = useState([]);
  const [charSkills, setCharSkills] = useState({
    Acrobatics: 2,
    Athletics: 2,
    Charm: 2,
    Combat: 2,
    Command: 2,
    'General Education': 2,
    'Medicine Education': 2,
    'Occult Education': 2,
    'Pokémon Education': 2,
    'Pokemon Education': 2,
    'Technology Education': 2,
    Focus: 2,
    Guile: 2,
    Intimidate: 2,
    Intuition: 2,
    Perception: 2,
    Stealth: 2,
    Survival: 2,
  });

  const levelUp = () => {
    charLevel < 50 ? setCharLevel(charLevel + 1) : console.log("LA LIASTE");
  };

  const levelDown = () => {
    charLevel > 1 ? setCharLevel(charLevel - 1) : console.log("LA LIASTE");
  };

  const addFeat = (featName) => {
    if(charFeatList.indexOf(featName) >=0){
      console.log("La liaste")
    } else
    setCharFeatList([...charFeatList, featName]);
  };

  const removeFeat = (featName) => {
    if(charFeatList.indexOf(featName) === -1){
      console.log("La liaste")
    } else
    setCharFeatList([...charFeatList.filter(feat => feat !== featName)]);
  };

  const upSkill = (skillName) => {
    const next = charSkills[skillName] + 1
    let hol = charSkills
    hol[skillName] = next
    setCharSkills({...hol})
  }

  function downSkill(skillName) {
    let next = charSkills[skillName] -1
    const hol = charSkills
    hol[skillName] = next
    setCharSkills({...hol})
  }

  const holder = [];

  for (let feat in jsonData.Features) {
    const specialHolder = jsonData.Features[feat].Prereq.Special;

    let skillOrHolder = null;
    let skillAndHolder = null;
    let featHolder = null;

    if (jsonData.Features[feat].Prereq.Skills) {
      skillOrHolder = jsonData.Features[feat].Prereq.Skills.Or
        ? jsonData.Features[feat].Prereq.Skills.Or
        : null;
      skillAndHolder = jsonData.Features[feat].Prereq.Skills.And
        ? jsonData.Features[feat].Prereq.Skills.And
        : null;
    }
    if (jsonData.Features[feat].Prereq.Feats) {
      featHolder = jsonData.Features[feat].Prereq.Feats
    }

    holder.push({
      Name: jsonData.Features[feat].Name,
      Effect: jsonData.Features[feat].Effect,
      Freq: jsonData.Features[feat].Freq,
      Tags: jsonData.Features[feat].Tags,
      Prereq: {
        Special: specialHolder,
        Skills: {
          Or: skillOrHolder,
          And: skillAndHolder,
        },
        Feats: featHolder,
      },
    });
  }

  function isAvailable(featName) {
    let truthHolder = []
    truthHolder.push(charFeatList.indexOf(featName) === -1)
    truthHolder.push(checkSkills(jsonData.Features[featName]))
    truthHolder.push(checkFeats(jsonData.Features[featName]))
    truthHolder.push(checkEdges(jsonData.Features[featName]))
    truthHolder.push(checkSpecial(jsonData.Features[featName]))
    return truthHolder.indexOf(false) === -1;
  }

  function checkSkills(feat){
    if (feat.Prereq.Skills){
      let truthHold = []
      if(feat.Prereq.Skills.And){
        for (let skill in feat.Prereq.Skills.And){
          truthHold.push(charSkills[skill] >= feat.Prereq.Skills.And[skill])
        }
      }
      if(feat.Prereq.Skills.Or){
        let passes = false
        for (let skill in feat.Prereq.Skills.Or){
          if (passes){}
          else
            passes = (charSkills[skill] >= feat.Prereq.Skills.Or[skill])
        }
        truthHold.push(passes)
      }
      return truthHold.indexOf(false) === -1;
    }else{
      return true
    }
  }

  function checkFeats(feat){
    if(feat['Prereq']['Feats']){
      let truthHold = []
      for (let thisFeat in feat.Prereq.Feats){
        truthHold.push(charFeatList.indexOf(feat.Prereq.Feats[thisFeat]) > -1)
        console.log(feat.Name,"--", feat.Prereq.Feats[thisFeat], "--", (charFeatList.indexOf(thisFeat) > -1))
      }
      return truthHold.indexOf(false) === -1;
    } else {
      return true
    }
  }

  function checkEdges(feat){
    if(feat.Prereq.Edges){
      let truthHold = []
      for (let thisFeat in feat.Prereq.Edges){
        truthHold.push(charEdgeList.indexOf(thisFeat) > -1)
      }
      return truthHold.indexOf(false) === -1;
    } else {
      return true
    }
  }

  function checkSpecial(feat){
    if(feat.Prereq.Special){
      return false;
    } else {
      return true;
    }
  }

  var skillPrinter = Object.keys(charSkills).map(function(key) {
    return <div value={key}>{key}:{ charSkills[key] }
      --
      <button onClick={() => upSkill(key)}>+</button>
      <button onClick={() => downSkill(key)}>-</button>
    </div>
});

  return (
    <section>
      <div className={classes.Builder}>
        Character Name:
        <div>
          Level : {charLevel} // <button onClick={levelUp}>Lvl Up</button> //{" "}
          <button onClick={levelDown}>Lvl Down</button>
        </div>
        <div>
          Feats:
          {charFeatList.map((feat) => (
            <div key={feat}>
              <button onClick={() => removeFeat(feat)}>{feat}</button>
            </div>
          ))}
        </div>
        <div>
          Edges: 
          {charEdgeList.map((edge) => (
            <div key={edge}>{edge}</div>
          ))}
        </div>
        <div>Skills:{charSkills.toString()}
          {skillPrinter}
        </div>
      </div>
      <p>/</p>
      {holder.map((feat) => (
        <div key={feat.Name}>
          {isAvailable(feat.Name) && (<a>--</a>) && (<a><button onClick={() => addFeat(feat.Name)}>{feat.Name}</button></a>)}
        </div>
      ))}
    </section>
  );
};

export default Builder;
/*
{holder.map((feat) => (
        <div key={feat.Name}>
          <FeatHolder
            Name={feat.Name}
            Effect={feat.Effect}
            Freq={feat.Freq}
            Tags={feat.Tags}
            Prereq={feat.Prereq}
          ></FeatHolder>
        </div>
      ))}
*/
