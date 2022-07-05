# Copyright (c) OpenMMLab. All rights reserved.
from unittest import TestCase

import torch
from torch import nn

from mmrazor.models.architectures.dynamic_op import (build_dynamic_bn,
                                                     build_dynamic_conv2d,
                                                     build_dynamic_gn,
                                                     build_dynamic_in,
                                                     build_dynamic_linear)


class TestDynamicLayer(TestCase):

    def test_dynamic_conv(self):
        imgs = torch.rand(2, 8, 16, 16)

        in_channels_cfg = dict(
            type='RatioChannelMutable',
            candidate_choices=[1 / 4, 2 / 4, 3 / 4, 1.0])

        out_channels_cfg = dict(
            type='RatioChannelMutable',
            candidate_choices=[1 / 4, 2 / 4, 3 / 4, 1.0])

        conv = nn.Conv2d(8, 8, 1)
        dynamic_conv = build_dynamic_conv2d(conv, 'op', in_channels_cfg,
                                            out_channels_cfg)
        # test forward
        dynamic_conv(imgs)

        conv = nn.Conv2d(8, 8, 1, groups=8)
        dynamic_conv = build_dynamic_conv2d(conv, 'op', in_channels_cfg,
                                            out_channels_cfg)
        # test forward
        dynamic_conv(imgs)

        conv = nn.Conv2d(8, 8, 1, groups=4)
        dynamic_conv = build_dynamic_conv2d(conv, 'op', in_channels_cfg,
                                            out_channels_cfg)
        # test forward
        with self.assertRaisesRegex(NotImplementedError,
                                    'only support pruning the depth-wise'):
            dynamic_conv(imgs)

    def test_dynamic_linear(self):
        imgs = torch.rand(2, 8)

        in_features_cfg = dict(
            type='RatioChannelMutable',
            candidate_choices=[1 / 4, 2 / 4, 3 / 4, 1.0])

        out_features_cfg = dict(
            type='RatioChannelMutable',
            candidate_choices=[1 / 4, 2 / 4, 3 / 4, 1.0])

        linear = nn.Linear(8, 8)
        dynamic_linear = build_dynamic_linear(linear, 'op', in_features_cfg,
                                              out_features_cfg)
        # test forward
        dynamic_linear(imgs)

    def test_dynamic_batchnorm(self):
        imgs = torch.rand(2, 8, 16, 16)

        num_features_cfg = dict(
            type='RatioChannelMutable',
            candidate_choices=[1 / 4, 2 / 4, 3 / 4, 1.0])

        bn = nn.BatchNorm2d(8)
        dynamic_bn = build_dynamic_bn(bn, 'bn', num_features_cfg)
        # test forward
        dynamic_bn(imgs)

        bn = nn.BatchNorm2d(8, momentum=0)
        dynamic_bn = build_dynamic_bn(bn, 'bn', num_features_cfg)
        # test forward
        dynamic_bn(imgs)

        bn = nn.BatchNorm2d(8)
        bn.train()
        dynamic_bn = build_dynamic_bn(bn, 'bn', num_features_cfg)
        # test forward
        dynamic_bn(imgs)
        # test num_batches_tracked is not None
        dynamic_bn(imgs)

        bn = nn.BatchNorm2d(8, affine=False)
        dynamic_bn = build_dynamic_bn(bn, 'bn', num_features_cfg)
        # test forward
        dynamic_bn(imgs)

        bn = nn.BatchNorm2d(8, track_running_stats=False)
        dynamic_bn = build_dynamic_bn(bn, 'bn', num_features_cfg)
        # test forward
        dynamic_bn(imgs)

    def test_dynamic_instancenorm(self):
        imgs = torch.rand(2, 8, 16, 16)

        num_features_cfg = dict(
            type='RatioChannelMutable',
            candidate_choices=[1 / 4, 2 / 4, 3 / 4, 1.0])

        instance_norm = nn.InstanceNorm2d(8)
        dynamic_in = build_dynamic_in(instance_norm, 'in', num_features_cfg)
        # test forward
        dynamic_in(imgs)

        instance_norm = nn.InstanceNorm2d(8, affine=False)
        dynamic_in = build_dynamic_in(instance_norm, 'in', num_features_cfg)
        # test forward
        dynamic_in(imgs)

        instance_norm = nn.InstanceNorm2d(8, track_running_stats=False)
        dynamic_in = build_dynamic_in(instance_norm, 'in', num_features_cfg)
        # test forward
        dynamic_in(imgs)

    def test_dynamic_groupnorm(self):
        imgs = torch.rand(2, 8, 16, 16)

        num_channels_cfg = dict(
            type='RatioChannelMutable',
            candidate_choices=[1 / 4, 2 / 4, 3 / 4, 1.0])

        gn = nn.GroupNorm(num_groups=4, num_channels=8)
        dynamic_gn = build_dynamic_gn(gn, 'gn', num_channels_cfg)
        # test forward
        dynamic_gn(imgs)

        gn = nn.GroupNorm(num_groups=4, num_channels=8, affine=False)
        dynamic_gn = build_dynamic_gn(gn, 'gn', num_channels_cfg)
        # test forward
        dynamic_gn(imgs)