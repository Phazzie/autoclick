# pylint: disable=redefined-outer-name,unused-argument
import pytest

from tools.plugin_generator import (
    InvalidPluginNameError,
    InvalidPluginTypeError,
    PluginConfig,
    PluginGenerator,
    PluginGeneratorError,
)


@pytest.fixture
def generator(tmp_path):
    return PluginGenerator(str(tmp_path))


@pytest.fixture
def valid_config():
    return PluginConfig(name="test_plugin", type="reporters")


def test_validate_plugin_name(generator):
    # Valid names
    generator.validate_plugin_name("valid_name")
    generator.validate_plugin_name("valid123")
    generator.validate_plugin_name("v")

    # Invalid names
    with pytest.raises(InvalidPluginNameError):
        generator.validate_plugin_name("Invalid")
    with pytest.raises(InvalidPluginNameError):
        generator.validate_plugin_name("123invalid")
    with pytest.raises(InvalidPluginNameError):
        generator.validate_plugin_name("invalid-name")


def test_validate_plugin_type(generator):
    # Valid types
    generator.validate_plugin_type("reporters")
    generator.validate_plugin_type("runners")
    generator.validate_plugin_type("storage")

    # Invalid types
    with pytest.raises(InvalidPluginTypeError):
        generator.validate_plugin_type("invalid_type")


def test_plugin_exists(generator, valid_config, tmp_path):
    plugin_path = tmp_path / "src" / "plugins" / "reporters" / "test_plugin.py"
    plugin_path.parent.mkdir(parents=True)
    plugin_path.touch()

    assert generator.plugin_exists(valid_config)


def test_create_plugin(generator, valid_config, tmp_path):
    # Test normal creation
    generator.create_plugin(valid_config)
    plugin_path = generator.get_plugin_path(valid_config)
    assert plugin_path.exists()

    # Test force overwrite
    config_with_force = PluginConfig(name="test_plugin", type="reporters", force=True)
    generator.create_plugin(config_with_force)

    # Test creation without force
    with pytest.raises(PluginGeneratorError):
        generator.create_plugin(valid_config)


def test_generate_plugin_content(generator, valid_config):
    content = generator.generate_plugin_content(valid_config)
    assert "class TestPluginPlugin(ReportersInterface):" in content
    assert "def __init__(self, config: Dict[str, Any]):" in content
