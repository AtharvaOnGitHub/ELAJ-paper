local labels = {}
for _, aux in ipairs({"main.aux", "supplementary.aux", "supplementary/supplementary.aux"}) do
  local f = io.open(aux)
  if f then
    for line in f:lines() do
      local k, v = line:match("^\\newlabel{([^}]+)}{{([^}]*)}")
      if k and labels[k] == nil then labels[k] = v end
    end
    f:close()
  end
end
function Image(el) return {} end
function Link(el)
  local t = pandoc.utils.stringify(el.content)
  local k = t:match("^%[(.+)%]$")
  if k and labels[k] then return pandoc.Str(labels[k]) end
end
