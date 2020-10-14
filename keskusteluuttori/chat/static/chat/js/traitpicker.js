const TRAIT_MAX=10;

$.fn.removeClassRegex = function(regex) {
  return $(this).removeClass((index, classes) => classes.split(/\s+/).filter(c => regex.test(c)).join(' '));
};

const load_speaker = speaker => (() => {
  const result = [];
  for (let key in speaker.traits) {
    const value = speaker.traits[key];
    result.push(renderTrait(key));
  }
  return result;
})();

const getTrait = function(element, field) {
  if (field == null) { field = "pk"; }
  return $(element).closest(".traitpicker").data("trait-"+field);
};

const getElement = function(trait, element) {
  if (element == null) { element = ".display"; }
  if (element ===".traitpicker") {
    return $(".traitpicker[data-trait-pk="+trait+"]");
  }
  return $(".traitpicker[data-trait-pk="+trait+"] " + element);
};

var renderTrait = function(trait) {
  let value = 0;
  let className = "neutral";
  const element = getElement(trait, '.traitpicker');
  const traitName = getTrait(element, "name");
  const oppositeName = getTrait(element, "opposite");
  let titleText = traitName + "/" + oppositeName;

  if (trait in SPEAKER.traits) {
    value = SPEAKER.traits[trait];
    if (value < 0) {
      className="cold-"+Math.abs(value);
      titleText=oppositeName;
    } else if (value > 0) {
      className="warm-"+value;
      titleText=traitName;
    }
  }
  const display=getElement(trait);
  display.html(Math.abs(value));
  display.removeClassRegex(/^color-/);
  display.addClass("color-"+className);
  const title=getElement(trait, '.title');
  title.removeClassRegex(/^color-/);
  title.addClass("color-"+className);
  return title.html(titleText);
};


const addToTrait = function(trait, value) {
  if (value == null) { value = 1; }
  if (!(trait in SPEAKER.traits)) {
    SPEAKER.traits[trait] = 0;
  }
  SPEAKER.traits[trait] = SPEAKER.traits[trait]+value;
  if (SPEAKER.traits[trait] > TRAIT_MAX) {
    SPEAKER.traits[trait]= TRAIT_MAX;
  }
  if (SPEAKER.traits[trait] < -TRAIT_MAX) {
    return SPEAKER.traits[trait] = -TRAIT_MAX;
  }
};
$(function() {
  load_speaker(SPEAKER);
  $(".controller .button.left").click(function() {
    const trait = getTrait(this);
    addToTrait(trait, -1);
    return renderTrait(trait);
  });

  return $(".controller .button.right").click(function() {
    const trait = getTrait(this);
    addToTrait(trait);
    return renderTrait(trait);
  });
});
