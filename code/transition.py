class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # Precondition: Neither the stack nor the buffer are empty
        # NOTE: This precondition is necessary
        if not conf.buffer or not conf.stack:
            return -1

        # Precondition: "wj" not already the dependent of another word
        # TODO: This precondition is not doing anything
        elif conf.stack[-1] in [dep[2] for dep in conf.arcs]:
            return -1

        idx_wi = conf.stack.pop()
        idx_wj = conf.buffer.pop(0)

        # Add to arcs
        conf.arcs.append((idx_wj, relation, idx_wi))

    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # Precondition: Neither the stack nor the buffer are empty
        if not conf.buffer or not conf.stack:
            return -1

        # You get this one for free! Use it as an example.

        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        conf.stack.append(idx_wj)
        conf.arcs.append((idx_wi, relation, idx_wj))

    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # Precondition: Neither the stack nor the buffer are empty
        # NOTE: This precondition does not seem to be necessary
        # if not conf.buffer or not conf.stack:
        #     return -1

        # Precondition: Word must be the dependent of another word
        if conf.stack[-1] not in [dep[2] for dep in conf.arcs]:
            return -1

        idx_wi = conf.stack[-1]

        conf.stack.remove(idx_wi)

    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # Precondition: The buffer is not empty
        # NOTE: This precondition does not seem to be necessary
        # if not conf.buffer:
        #     return -1

        # Word at the top of the buffer moved to the stack
        idx_wj = conf.buffer.pop(0)
        conf.stack.append(idx_wj)
