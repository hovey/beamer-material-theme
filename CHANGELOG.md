# Changelog

## 3.0.0

### Added

- Dockerization of the build-process
- `darkpurple` theme to `config.lua`

### Changed

- build-system `rake` to `LuaTeX` (removed python code and replaced it with lua)
- `config.json` to `config.lua`

## 2.1.0

### Added

- Command `\topicFramePrimary[subtitle]{Title}` which creates a topic-introduction frame with primary color as background
- Command `\topicFrameSecondary[subtitle]{Title}` which creates a topic-introduction frame with secondary color as background

## 2.0.1

### Added

- Page number to navigation symbols
- Example pdf

### Changed

- Caption color
- `\sidebysideX` layout's first optional argument specifies the ratio of the sides
- Updated readme + example slides

## 2.0.0

### Added

- Side by side slides
- Build system

### Fixed

- Shadow was not displayed correctly in some cases, added a guideline

### Changed

- Folder structure improvements
- Theme generation is now done with

    ```bash
    rake setup
    rake default
    ```

- Theme settings are done in the `config.json` file

## 1.0.0

Initial release featuring:

- Theme customization via `LaTeX` commands
- Material Design
