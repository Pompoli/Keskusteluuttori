TRAIT_MAX=10

$.fn.removeClassRegex = (regex) ->
  $(@).removeClass (index, classes) ->
    classes.split(/\s+/).filter (c) ->
      regex.test c
    .join ' '

load_speaker = (speaker) ->
  for key, value of speaker.traits
    renderTrait key

getTrait = (element, field = "pk") ->
  return $(element).closest(".traitpicker").data("trait-"+field)

getElement = (trait, element=".display") ->
  if element ==".traitpicker"
    return $(".traitpicker[data-trait-pk="+trait+"]")
  return $(".traitpicker[data-trait-pk="+trait+"] " + element)

renderTrait = (trait) ->
  value = 0
  className = "neutral"
  element = getElement(trait, '.traitpicker')
  traitName = getTrait(element, "name")
  oppositeName = getTrait(element, "opposite")
  titleText = traitName + "/" + oppositeName

  if trait of SPEAKER.traits
    value = SPEAKER.traits[trait]
    if value < 0
      className="cold-"+Math.abs(value)
      titleText=oppositeName
    else if value > 0
      className="warm-"+value
      titleText=traitName
  display=getElement(trait)
  display.html(Math.abs(value))
  display.removeClassRegex(/^color-/)
  display.addClass("color-"+className)
  title=getElement(trait, '.title')
  title.removeClassRegex(/^color-/)
  title.addClass("color-"+className)
  title.html titleText


addToTrait = (trait, value=1) ->
  if trait not of SPEAKER.traits
    SPEAKER.traits[trait] = 0
  SPEAKER.traits[trait] = SPEAKER.traits[trait]+value
  if SPEAKER.traits[trait] > TRAIT_MAX
    SPEAKER.traits[trait]= TRAIT_MAX
  if SPEAKER.traits[trait] < -TRAIT_MAX
    SPEAKER.traits[trait] = -TRAIT_MAX
$ ->
  load_speaker SPEAKER
  $(".controller .button.left").click ->
    trait = getTrait(this)
    addToTrait trait, -1
    renderTrait trait

  $(".controller .button.right").click ->
    trait = getTrait(this)
    addToTrait trait
    renderTrait trait
